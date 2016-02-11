import xml.etree.ElementTree as etree
import re

def read_action(element):
	"""Liest eine Veränderung im Lehrer-Vertretungsplan"""

	get = lambda tag: element.find(tag).text
	# Liest den Text aus einem Element
	# raised einen AttributeError falls tag nicht vorhanden.
	
	try:
		old = {
			'subject': get('fach'),
			'teacher': get('lehrer')
		}
		new = {
			'subject': get('vfach'),
			'teacher': get('vlehrer'),
			'room': get('vraum')
		}

		change = 'info'
		if old['subject'] != new['subject']: change = 'subject'
		if old['teacher'] != new['teacher']: change = 'teacher'
		# Am Ende falls Ausfall, werden alle vorherigen Flags überschrieben.
		if new['subject'] == '---': change = 'cancelled'

		if not change and not get('info'): change = 'room'
		# not change besagt, dass change leer ist, also keine Änderung in Fach und Lehrer. Ist weiterhin
		# keine Info vorhanden ( not get('info') ), dann kann es sich nur um eine Raumänderung handeln

		return {
			'class': parse_class( get('klasse') ),
			'time': get('stunde'),
			'info': get('info'),
			'old': old,
			'new': new,
			'change': change
		}

	except AttributeError:
		return None

def parse_class(text):
	lower_class_simple = re.compile( r'^(?P<grade>0[5-9]|10)(?P<subgrade>[A-D])$' )
	lower_class_multiple_inter = re.compile( r'^(.*)/ (?P<grade>0[5-9]|10)(?P<subject>[A-Z]{2,3})(?P<subclass>\d)$' ) # 08FRZ1
	higher_class_simple = re.compile( r'^(?P<grade>11|12)/ (?P<subject>[a-z]{2})(?P<subclass>\d)$' )

	return text

def _parse_lower_class_simple(match):
	return match.groupdict()

def convert(xml_content):
	"""Konvertiert einen xml-String in ein dictionary"""
	if not xml_content:
		return None

	try:
		root = etree.fromstring(xml_content)

	except etree.ParseError:
		return None

	events = []
	for element in root.findall('./haupt/aktion'):
		event = read_action(element)

		if event:
			events.append(event)

		else:
			return None

	return {'events': events}
