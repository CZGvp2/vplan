import re
from datetime import datetime
import locale
import logging

log = logging.getLogger('serverlog')


# Setzen des Datumsformats von Deutscherland
locale.setlocale(locale.LC_TIME, 'deu_deu')  # TODO fehler auf Unix?


# 08A, 10B usw.
SIMPLE = re.compile( r'^(0[5-9]|10)[A-D]$' )

# Klassenübergreifend. Bsp: "08A,08B,08C/ 08FRZ2", "06A,06B/ 06ABET", "10C/ 10CIF2"
MULT = re.compile( r'^(?P<targets>((0[5-9]|10)[A-D],?)+)/\s(?P<classes>(0[5-9]|10)[A-D]{,4})(?P<subject>[A-Z]{2,})(?P<subclass>\d)?$' )

# Kurssystem Bsp.: 11/ ma2  oder 12/ de1
COURSE = re.compile( r'^(?P<grade>11|12)/\s(?P<subject>[a-z]{2,})(?P<subclass>\d)$' )


lower = lambda text: (text[1:] if text[0] == '0' else text).lower() # '08' -> '8', oder '09B' -> '9b'

def parse_simple(text):
	match = SIMPLE.match(text)
	if not match:
		return None

	_class = lower(text)
	return {
		'type': 'SIMPLE',
		'class': _class,
		'targets': [_class]
	}

def parse_mult(text):
	match = MULT.match(text)
	if not match:
		return None

	return {
		'type': 'MULT',
		'classes': lower( match.group('classes') ),
		'subject': replace_subject( match.group('subject') ),
		'subclass': match.group('subclass'),
		'targets': list( map(lower, match.group('targets').split(',')) )  # '08A,08B,08C' zu ['8a', '8b', '8c']
	}

def parse_course(text):
	match = COURSE.match(text)
	if not match:
		return None

	data = match.groupdict()  # hat grade und subclass gleich drin

	# Hinzufügen der weiteren Daten
	data['type'] = 'COURSE'
	data['subject'] = replace_subject( match.group('subject') )
	data['targets'] = [ match.group('grade') ]

	return data

def parse_selector(text):
	"""Parst einen Klassen-Bezeichner in JSON"""

	for parser in (parse_simple, parse_mult, parse_course):
		data = parser(text)

		if data:
			return data

	log.warning('Could not parse class "%s"', text)
	return {
		'type': 'FAILED',
		'class': text,
		'targets': []
	} #  Als Backup falls das Parsen nirgends funktioniert hat

def replace_subject(text):
	"""Parst ein Fach in JSON """
	return text  # TODO du weißt was

def parse_date(text):
	"""Parst das Datum der Datei aus text zu JSON"""

	date = datetime.strptime(text, '%A, %d. %B %Y')
	return {
		'day': date.day,
		'month': date.month,
		'year': date.year
	}
	 # TODO  Error User info + log

def parse_response_date(date):
	"""Parst das Datum für die Ajax Response"""
	date = datetime(**date)

	return {
		'weekday': date.strftime('%A'),
		'date': date.strftime('%d. %B %Y')
	}