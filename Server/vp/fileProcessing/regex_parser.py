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
SIMPLE = re.compile( r'^(?P<grade>0[5-9]|10)(?P<subgrade>[A-D])$' )

# Klassenübergreifend. Bsp: "08A,08B,08C/ 08FRZ2", "06A,06B/ 06ABET", "10C/ 10CIF2"
MULT = re.compile( r'^(?P<targets>((0[5-9]|10)[A-D],?)+)/\s(?P<classes>(?P<grade>0[5-9]|10)[A-D]{,4})(?P<subject>[A-Z]{2,})(?P<subclass>\d)?$' )

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
to_int = lambda text: None if not text else int(text)

class Selector:
	"""Bezeichner für die Klassen"""
	def __init__(self, text):
		parsers = [
			('SIMPLE', self.parse_simple),
			('MULT', self.parse_mult),
			('COURSE', self.parse_course)
		]

		self.type = 'FAILED'

		for type, parser in parsers:
			if parser(text):
				self.type = type
				break

		if self.type == 'FAILED':
			log.warning('Could not parse class "%s"', text)
			self.text = text
			self.targets = ('notset', )

	def parse_simple(self, text):
		"""Einfacher Ausdruck, wie 8C oder 10C"""
		match = SIMPLE.match(text)
		if not match:
			return False

		self.grade = int( match.group('grade') )
		self.subgrade = match.group('subgrade').lower()
		self.targets = (lower(text), )

		return True

	def parse_mult(self, text):
		"""Parst einen auf mehrere Klassen verweisenden Ausdruck."""
		match = MULT.match(text)
		if not match:
			return False

		self.classes = lower( match.group('classes') )
		self.grade = int( match.group('grade') )
		self.subject = replace_subject( match.group('subject') )
		self.subclass = to_int( match.group('subclass') )
		self.targets = tuple( map(lower, match.group('targets').split(',')) )  # '08A,08B,08C' zu ('8a', '8b', '8c')

		return True

	def parse_course(self, text):
		"""Parst einen Kurs"""
		match = COURSE.match(text)
		if not match:
			return False # hat grade und subclass gleich drin

		self.grade = int( match.group('grade') )
		self.subject = match.group('subject')
		self.subclass = to_int( match.group('subclass') )
		self.targets = (str(self.grade), )

		return True

	def json(self):
		data = self.__dict__.copy()
		data.pop('targets')
		return data

	def get_z(self):
		"""Gibt einen Wert zum Sortieren zurück"""
		if self.type == 'FAILED':
			return 500  # ganz groß

		order = 'SIMPLE', 'MULT', 'COURSE'

		return 100*order.index(self.type) + self.grade


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