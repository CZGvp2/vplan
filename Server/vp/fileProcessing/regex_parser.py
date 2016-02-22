import re
import os.path
from datetime import datetime
import locale
import logging

from .exceptions import IOServerError, InternalServerError, ProcessingError


log = logging.getLogger('serverlog')

# Setzen des Datumsformats von Deutscherland
locale.setlocale(locale.LC_TIME, 'deu_deu')  # TODO fehler auf Unix?


# 08A, 10B usw.
SIMPLE = re.compile( r'^(0[5-9]|10)[A-D]$' )

# Klassenübergreifend. Bsp: "08A,08B,08C/ 08FRZ2", "06A,06B/ 06ABET", "10C/ 10CIF2"
MULT = re.compile( r'^(?P<targets>((0[5-9]|10)[A-D],?)+)/\s(?P<classes>(0[5-9]|10)[A-D]{,4})(?P<subject>[A-Z]{2,})(?P<subclass>\d)?$' )

# Kurssystem Bsp.: 11/ ma2  oder 12/ de1
COURSE = re.compile( r'^(?P<grade>11|12)/\s(?P<subject>[a-z]{2,})(?P<subclass>\d)$' ) # TODO spezielles Parsen

# Lehrer, passt sowohl mit als auch ohne Klammern. Bsp.: "MUE", "(REN)"
TEACHER = re.compile( r'^\(?([A-ZÄÖÜ]{2,})\)?$' )

# TODO AG

# Laden der subjects.data TODO (sollte jedes mal beim Uploaden passieren)
subjects_file = os.path.normpath( os.path.join( os.path.dirname(__file__), '../data/subjects.data' ) )
subjects = {}
try:
	with open(subjects_file, 'r') as fobj:
		for lineno, line in enumerate( fobj.readlines() ):
			name, replacement = tuple( line[:-1].split(' ') ) # :-1 entfernt den letzten character, \n
			subjects[name] = replacement

except IOError:
	raise IOServerError(subjects_file)

except ValueError:
	raise InternalServerError('Invalid Syntax in subjects.data line %(lineno)d "%(line)s"', lineno=lineno, line=lines)


lower = lambda text: (text[1:] if text[0] == '0' else text).lower() # '08' -> '8', oder '09B' -> '9b'

def parse_simple(text):
	match = SIMPLE.match(text)
	if not match:
		return None, ()

	_class = lower(text)
	return {
		'type': 'SIMPLE',
		'class': _class,
	}, (_class,)

def parse_mult(text):
	"""Parst einen auf mehrere Klassen verweisenden Ausdruck. Gibt JSON und tupel von targets zurück."""
	match = MULT.match(text)
	if not match:
		return None, ()

	data = {
		'type': 'MULT',
		'classes': lower( match.group('classes') ),
		'subject': replace_subject( match.group('subject') ),
		'subclass': match.group('subclass')
	}
	targets = tuple( map(lower, match.group('targets').split(',')) )  # '08A,08B,08C' zu ['8a', '8b', '8c']

	return data, targets

def parse_course(text):
	match = COURSE.match(text)
	if not match:
		return None, ()

	data = match.groupdict()  # hat grade und subclass gleich drin

	# Hinzufügen der weiteren Daten
	data['type'] = 'COURSE'
	data['subject'] = replace_subject( match.group('subject') )

	return data, ( match.group('grade'), )

def parse_selector(text):
	"""Parst einen Klassen-Bezeichner in JSON, gibt data und targets zurück"""

	for parser in (parse_simple, parse_mult, parse_course):
		data, targets = parser(text)

		if data:
			return data, targets

	log.warning('Could not parse class "%s"', text)
	return {
		'type': 'FAILED',
		'class': text
	}, ()

def replace_subject(text):
	"""Ersetzt ein Fach."""
	if text == '---':
		return None

	try:
		return subjects[ text.lower() ]

	except KeyError:
		log.warning('Could not replace subject "%s"', text)
		return text.capitalize()

def replace_teacher(text):
	"""Übersetzt einen Lehrer. Klammern werden entfernt, Anfangsbuchstabe groß"""
	if text == '---':
		return None

	match = TEACHER.match(text)
	if not match:
		log.warning('Could not replace teacher "%s"', text)
		return text.capitalize()

	return match.group(1).capitalize()

def parse_date(text):
	"""Parst das Datum der Datei aus text zu JSON"""
	try:
		date = datetime.strptime(text, '%A, %d. %B %Y')
		return {
			'day': date.day,
			'month': date.month,
			'year': date.year
		}

	except ValueError:
		raise ProcessingError('ERR_PARSING_DATE', 'Could not parse date "%(date)s"', date=text)

def parse_response_date(date):
	"""Parst das Datum für die Ajax Response"""
	date = datetime(**date)

	return {
		'weekday': date.strftime('%A'),
		'date': date.strftime('%d. %B %Y')
	}