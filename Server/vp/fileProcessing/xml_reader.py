import xml.etree.ElementTree as etree

from .serverlog import ProcessingError
from .regex_parser import Selector, parse_date, parse_subject, replace_teacher, dashToNone

NONE_SUBJ = {
	'prefix': None,
	'subject': None,
	'suffix': None
}

def convert(xml_content):
	"""Konvertiert einen xml-String in ein dictionary, Ergebnis sind JSON-Daten für einen Tag"""

	try:
		# Parsen vom String xml_content
		root = etree.fromstring(xml_content)

	except etree.ParseError as e:
		raise ProcessingError('ERR_PARSING_XML', 'Could not parse XML')

	filename = get(root, './kopf/datei')
	date = parse_date( get(root, './kopf/titel') )

	events = []
	for action in root.findall('./haupt/aktion'):
		new_event = Event(action)

		merged = False
		for event in events:
			if new_event.is_next(event):
				event.merge(new_event)
				merged = True
				break

		if not merged:
			events.append(new_event)

	events.sort(key=Event.get_z)  # je größer der Wert vom event, desto höher steht es in der liste

	return {
		'events': [event.json() for event in events],
		'filename': filename,
		'date': date
	}

class Event:
	"""Eintrag im Lehrer-Vertretungsplan"""
	def __init__(self, action):
		# Erspart Tipparbeit, da in dieser Funktion get immer vom element ausgeht
		get_tag = lambda tag: get(action, tag)

		# Selektor der Klasse(n)
		self.selector = Selector( get_tag('klasse') )
		is_course = self.selector.grade >= 11

		# Alte Stunde
		self.old = {
			'subject': parse_subject( get_tag('fach'), course=is_course  ),
			'teacher': replace_teacher( get_tag('lehrer') ),
		}

		# Neue Stunde
		self.new = {
			'subject': parse_subject( get_tag('vfach'), course=is_course ),
			'teacher': replace_teacher( get_tag('vlehrer') ),
			'room': dashToNone( get_tag('vraum') )
		}

		self.info = get_tag('info')
		self.time = [ int( get_tag('stunde') ) ]  # time ist liste von allen Stunden mit gleichen Infos

		self.change = None
		if self.old['teacher'] != self.new['teacher']: self.change = 'TEACHER'
		if self.old['subject'] != self.new['subject']: self.change = 'SUBJECT'
		# Am Ende falls Ausfall, werden alle vorherigen Flags überschrieben.

		if self.new['subject'] == NONE_SUBJ:
			self.change = 'CANCELLED'

		if not self.change: self.change = 'ROOM'
		# not change besagt, dass change leer ist, also keine Änderung in Fach und Lehrer.
		# daher kann es sich nur um eine Raumänderung handeln

		self.targets = self.selector.targets

		# Hinzufügen der Lehrer zu den Targets
		if self.old['teacher']:
			self.targets.append(self.old['teacher'])  # Falls Teacher '---' und damit None, nicht hinzufügen

		if self.new['teacher'] and self.new['teacher'] not in self.targets:
			self.targets.append(self.new['teacher'])

		# Löschen von unnützen Daten
		if self.change == 'CANCELLED':
			self.new['subject'] = NONE_SUBJ
			self.new['teacher'] = None

		elif self.change == 'TEACHER':
			self.old['subject'] = NONE_SUBJ

		elif self.change == 'ROOM':
			self.old['teacher'] = None
			self.old['subject'] = NONE_SUBJ


	def get_z(self):
		"""Gibt einen numerischen Wert zum Sortieren zurück"""

		return 10*self.selector.get_z() + max(self.time)

	def is_next(self, other):
		"""Falls es sich um die gleiche Änderung in der darauffolgenden Stunde handelt"""
		return (self.old, self.new, self.selector) == (other.old, other.new, other.selector)

	def merge(self, other):
		"""Hinzufügen von Zeit des anderen Events zu eigenem Event"""
		if other.time[0] not in self.time:
			self.time.append(other.time[0])

	def json(self):
		"""JSON Representation des Events"""

		data = self.__dict__.copy()
		data['selector'] = self.selector.json()  # Selektor als dictionary
		data['targets'] = ' '.join(self.selector.targets)  # Liste zu String mit Leerzeichen machen
		data['time'] = ', '.join( map(str, self.time) )  # Liste zu String mit Kommas machen

		return data


def get(element, path):
	"""Gibt den Inhalt eines XML-Tags an der Postition path ausgehend vom Ursprung element an"""
	target = element.find(path)

	if target is None:
		raise ProcessingError('ERR_READING_XML', 'Could not find tag "%(path)s"', path=path)

	return target.text
