import xml.etree.ElementTree as etree
import re
import logging

from .exceptions import XMLReadingError, XMLParsingError


log = logging.getLogger('serverlog')


# Bsp: Montag, 19. Oktober 2015
date_syntax = re.compile( r'^(?P<dow>Montag|Dienstag|Mittwoch|Donnerstag|Freitag),\s(?P<date>.+)$' )

class_syntax = {
	# 08A, 10B usw.
	'lower_class_simple': re.compile( r'^(?P<grade>0[5-9]|10)(?P<subgrade>[A-D])$' ),

	# Klassen aus mehreren Klassen. Bsp: "08A,08B,08C/ 08FRZ2"
	'lower_class_mult': re.compile( r'^((0[5-9]|10)[A-D],?)?/\s(?P<grade>0[5-9]|10)(?P<subject>[A-Z]{2,})(?P<subclass>\d)$' ),

	# Klassen die in Gruppen geteilt sind: 10C/ 10CIF2
	'lower_class_split': re.compile( r'^(?P<class>(0[5-9]|10)[A-D])/\s(?P=class)(?P<subject>[A-Z]{2,})(?P<subclass>\d)$' ),

	# Kurssystem Bsp.: 11/ ma2  oder 12/ de1
	'higher_class': re.compile( r'^(?P<grade>11|12)/\s(?P<subject>[a-z]{2,})(?P<subclass>\d)$' )
}

def get(element, path):
	target = element.find(path)

	if target is not None:
		return target.text

	else:
		raise XMLReadingError(path)

def read_action(element):
	"""Liest eine Veränderung im Lehrer-Vertretungsplan"""

	get_tag = lambda tag: get(element, tag)

	old = {
		'subject': get_tag('fach'),
		'teacher': get_tag('lehrer')
	}
	new = {
		'subject': get_tag('vfach'),
		'teacher': get_tag('vlehrer'),
		'room': get_tag('vraum')
	}

	change = 'info'
	if old['subject'] != new['subject']: change = 'subject'
	if old['teacher'] != new['teacher']: change = 'teacher'
	# Am Ende falls Ausfall, werden alle vorherigen Flags überschrieben.
	if new['subject'] == '---': change = 'cancelled'

	if not change and not get_tag('info'): change = 'room'
	# not change besagt, dass change leer ist, also keine Änderung in Fach und Lehrer. Ist weiterhin
	# keine Info vorhanden ( not get('info') ), dann kann es sich nur um eine Raumänderung handeln

	return {
		'class': parse_class( get_tag('klasse') ),
		'time': get_tag('stunde'),
		'info': get_tag('info'),
		'old': old,
		'new': new,
		'change': change
	}

def parse_class(text):
	return text

def _parse_lower_class_simple(text):
	"""Parst einen Klassen-Bezeichner in JSON"""
	for typ, syntax in class_syntax.items():
		match = syntax.match(text)
		if match:
			data = match.groupdict()
			data['type'] = typ

			return data

	log.warning('Could not parse class "%s"', text)
	return {
		'type': None,
		'class': text
	} # Als Backup falls das Parsen nirgends funktioniert hat

def parse_subject(text):
	"""Parst ein Fach in JSON"""
	pass

def parse_date(text):
	match = date_syntax.match(text)

	if match:
		return match.groupdict()

	log.warning('Could not parse date "%s"' % text)
	return text

def convert(xml_content):
	"""Konvertiert einen xml-String in ein dictionary, Ergebnis sind JSON-Daten für einen Tag
	   gibt (data, errorCode) als Tupel zurück
	"""

	try:
		root = etree.fromstring(xml_content)

	except etree.ParseError as e:
		raise XMLParsingError(e)

	filename = get(root, './kopf/datei')
	date = parse_date( get(root, './kopf/titel') )

	events = []
	for element in root.findall('./haupt/aktion'):
		event = read_action(element)
		events.append(event)

	return {
		'events': events,
		'filename': filename,
		'date': date
	}
		
