import xml.etree.ElementTree as etree

from .serverlog import ProcessingError
from .regex_parser import Selector, parse_date, replace_subject, replace_teacher


def convert(xml_content):
	"""Konvertiert einen xml-String in ein dictionary, Ergebnis sind JSON-Daten für einen Tag
	   gibt (data, errorCode) als Tupel zurück"""

	try:
		# Parsen vom String xml_content
		root = etree.fromstring(xml_content)

	except etree.ParseError as e:
		raise ProcessingError('XML_PARSING_ERROR', 'Could not parse XML')

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

		# Alte Stunde
		self.old = {
			'subject': replace_subject( get_tag('fach') ),
			'teacher': replace_teacher( get_tag('lehrer') )
		}

		# Neue Stunde
		self.new = {
			'subject': replace_subject( get_tag('vfach') ),
			'teacher': replace_teacher( get_tag('vlehrer') ),
			'room': None if get_tag('vraum') == '---' else get_tag('vraum')
		}

		self.info = get_tag('info')
		self.time = [ int( get_tag('stunde') ) ]  # time ist liste von allen Stunden mit gleichen Infos

		self.change = None
		if self.old['teacher'] != self.new['teacher']: self.change = 'TEACHER'
		if self.old['subject'] != self.new['subject']: self.change = 'SUBJECT'
		# Am Ende falls Ausfall, werden alle vorherigen Flags überschrieben.
		if not self.new['subject']:
			self.change = 'CANCELLED'

		if not self.change: self.change = 'ROOM'
		# not change besagt, dass change leer ist, also keine Änderung in Fach und Lehrer.
		# daher kann es sich nur um eine Raumänderung handeln

		self.selector = Selector( get_tag('klasse') )
		self.targets = self.selector.targets

		# Hinzufügen der Lehrer zu den Targets
		if self.old['teacher']:
			self.targets += ( self.old['teacher'], )  # Falls Teacher '---' und damit None, nicht hinzufügen

		if self.new['teacher'] and self.new['teacher'] not in self.targets:
			self.targets += ( self.new['teacher'], )


	def get_z(self):
		"""Gibt einen numerischen Wert zum Sortieren zurück"""

		return 10*self.selector.get_z() + min(self.time)

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
		data['selector'] = self.selector.json()

		return data


def get(element, path):
	"""Gibt den Inhalt eines XML-Tags an der Postition path ausgehend vom Ursprung element an"""
	target = element.find(path)

	if target is None:
		raise ProcessingError('XML_READING_ERROR', 'Could not find tag "%(path)s"', path=path)

	return target.text
