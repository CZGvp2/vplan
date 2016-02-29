import xml.etree.ElementTree as etree
import logging

from .exceptions import XMLReadingError, XMLParsingError
from .regex_parser import parse_selector, parse_date, replace_subject, replace_teacher


log = logging.getLogger('serverlog')


def convert(xml_content):
	"""Konvertiert einen xml-String in ein dictionary, Ergebnis sind JSON-Daten für einen Tag
	   gibt (data, errorCode) als Tupel zurück"""

	try:
		# Parsen vom String xml_content
		root = etree.fromstring(xml_content)

	except etree.ParseError as e:
		raise XMLParsingError(e)

	filename = get(root, './kopf/datei')
	date = parse_date( get(root, './kopf/titel') )

	events = []
	for action in root.findall('./haupt/aktion'):
		event = read_action(action)
		events.append(event)

	return {
		'events': events,
		'filename': filename,
		'date': date
	}

def get(element, path):
	"""Gibt den Inhalt eines XML-Tags an der Postition path ausgehend vom Ursprung element an"""
	target = element.find(path)

	if target is None:
		raise XMLReadingError(path)

	return target.text

def read_action(element):
	"""Liest eine Veränderung im Lehrer-Vertretungsplan"""

	# Erspart Tipparbeit, da in dieser Funktion get immer vom element ausgeht
	get_tag = lambda tag: get(element, tag)

	# Alte Stunde
	old = {
		'subject': replace_subject( get_tag('fach') ),
		'teacher': replace_teacher( get_tag('lehrer') )
	}

	# Neue Stunde
	new = {
		'subject': replace_subject( get_tag('vfach') ),
		'teacher': replace_teacher( get_tag('vlehrer') ),
		'room': get_tag('vraum')
	}

	change = 'INFO'
	if old['subject'] != new['subject']: change = 'SUBJECT'
	if old['teacher'] != new['teacher']: change = 'TEACHER'
	# Am Ende falls Ausfall, werden alle vorherigen Flags überschrieben.
	if new['subject'] == '---':
		change = 'CANCELLED'

	if not change and not get_tag('info'): change = 'ROOM'
	# not change besagt, dass change leer ist, also keine Änderung in Fach und Lehrer. Ist weiterhin
	# keine Info vorhanden ( not get('info') ), dann kann es sich nur um eine Raumänderung handeln

	selector, targets = parse_selector( get_tag('klasse') )
	if old['teacher']:
		targets += ( old['teacher'], )  # Falls Teacher '---' und damit None, nicht hinzufügen

	if new['teacher'] and new['teacher'] not in targets:
		targets += ( new['teacher'], )
	
	return {
		'selector': selector,
		'targets': targets,
		'time': get_tag('stunde'),
		'info': get_tag('info'),
		'old': old,
		'new': new,
		'change': change
	}