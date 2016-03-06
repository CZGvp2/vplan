import re
import os.path
from datetime import datetime
import locale

from .serverlog import log, InternalServerError, ProcessingError


# Setzen des Datumsformats von Deutscherland
locale.setlocale(locale.LC_TIME, 'deu_deu')  # TODO fehler auf Unix?


# 08A, 10B usw.
SIMPLE = re.compile( r'^(?P<grade>0[5-9]|10)(?P<subgrade>[A-D])$' )

# Klassenübergreifend. Bsp: "08A,08B,08C/ 08FRZ2", "06A,06B/ 06ABET", "10C/ 10CIF2"
MULT = re.compile( r'^(?P<targets>((0[5-9]|10)[A-D],?)+)/\s(?P<grade>0[5-9]|10)(?P<subgrades>[A-D]{,4})?(?P<subject>(WOU|AG)?[a-zA-Z]{2,3})(?P<subclass>\d)?$' )

# Kurssystem Bsp.: 11/ ma2  oder 12/ ene
COURSE = re.compile( r'^(?P<grade>11|12)(/\s(?P<subject>[a-z]{2,})(?P<subclass>\d)?)?$' ) # TODO spezielles Parsen

# Passt auf alle WoUs (schon lower) z.B: wouma, wouif, wou
# Passt auf AGs z. B. agm, ag
# Passt auf Kurs z. B. en, ma, ene, biz
# gibt Prefix, Fach und Suffix in match
SUBJECT = re.compile( r'^(?P<prefix>wou|ag)?(?P<subject>[a-z]{2,3})(?P<suffix>[ez]){0}$' ) # 2-3, kein Suffix (das meiste)
SUBJECT_COURSE = re.compile( r'^(?P<prefix>)(?P<subject>[a-z]{2})(?P<suffix>[ez])?$' ) # 2 zeichen lang, opt. Suffix

# Laden der subjects.data TODO (sollte jedes mal beim Uploaden passieren)
subjects_file = os.path.normpath( os.path.join( os.path.dirname(__file__), '../data/subjects.data' ) )
subjects = {}
try:
	with open(subjects_file, 'r') as fobj:
		for lineno, line in enumerate( fobj.readlines() ):
			name, replacement = tuple( line[:-1].split(' ') ) # :-1 entfernt den letzten character, \n
			subjects[name] = replacement

except FileNotFoundError:
	raise InternalServerError("IO Error reading subjects")

except ValueError:
	raise InternalServerError('Invalid Syntax in subjects.data line %(lineno)d "%(line)s"', lineno=lineno, line=lines)


lower = lambda text: (text[1:] if text[0] == '0' else text).lower() # '08' -> '8', oder '09B' -> '9b'
to_int = lambda text: None if not text else int(text)
dashToNone = lambda text: None if text == "---" else text # gibt None zurück falls text == "---"

class Selector:
	"""Bezeichner für die Klassen"""
	def __init__(self, text):
		parsers = [
			('SIMPLE', self.parse_simple),
			('MULT', self.parse_mult),
			('COURSE', self.parse_course)
		]

		self.grade = 0
		self.subgrades = None
		self.subclass = None
		self.subject = {
			'prefix': None,
			'subject': None,
			'suffix': None
		}

		self.targets = ['notset']
		self.type = 'FAILED'

		for type, parser in parsers:
			if parser(text):
				self.type = type
				break

		if self.type == 'FAILED':
			log.warning('Could not parse class "%s"', text)
			self.text = text

	def parse_simple(self, text):
		"""Einfacher Ausdruck, wie 8C oder 10C"""
		match = SIMPLE.match(text)
		if not match:
			return False

		self.grade = int( match.group('grade') )
		self.subgrades = match.group('subgrade').lower()
		self.targets = [ lower(text) ]

		return True

	def parse_mult(self, text):
		"""Parst einen auf mehrere Klassen verweisenden Ausdruck."""
		match = MULT.match(text)
		if not match:
			return False

		self.subgrades = match.group('subgrades').lower()
		self.grade = int( match.group('grade') )
		self.subject = parse_subject( match.group('subject'), course=False )
		self.subclass = to_int( match.group('subclass') )
		self.targets = list( map(lower, match.group('targets').split(',')) )  # '08A,08B,08C' zu ('8a', '8b', '8c')

		return True

	def parse_course(self, text):
		"""Parst einen Kurs"""
		match = COURSE.match(text)
		if not match:
			return False # hat grade und subclass gleich drin

		self.grade = int( match.group('grade') )
		self.subject = parse_subject( match.group('subject'), course=True )
		self.subclass = to_int( match.group('subclass') )
		self.targets = [ str(self.grade) ]

		return True

	def __eq__(self, other):
		"""Vergleichsfunktion für den gleichen Selektor"""
		return self.__dict__ == other.__dict__

	def json(self):
		"""JSON Representation des Events"""
		data = self.__dict__.copy()

		# Entfernen von Targets
		data.pop('targets')

		return data

	def get_z(self):
		"""Gibt einen Wert zum Sortieren zurück"""

		if self.type == 'FAILED':
			return 5000  # ganz groß

		return 10*self.grade \
			+ 4*('SIMPLE', 'MULT', 'COURSE').index(self.type) \
			+ (0 if not self.subgrades else 'abcd'.index(self.subgrades[0]) )


def parse_subject(text, course=False):
	"""Ersetzt ein Fach und versucht es in Präfix, Fach und Suffix zu Unterteilen"""

	prefix = None
	suffix = None

	if not text or text == '---':
		subject = None

	else:
		match = (SUBJECT_COURSE if course else SUBJECT).match( text.lower() )

		if not match:
			if course:
				log.warning('Could not match subject "%s"', text)
				subject = text

			else:  # Wenn nicht Kurz geparst werden konnte, versuche Kurs zu Parsen
				return parse_subject(text, course=True)

		else:
			prefix, subject, suffix = match.groups()
			try:
				subject = subjects[ subject.lower() ]  # Ersetzen durch Daten aus subject.data

			except KeyError:
				log.warning('Could not replace subject "%s"', text)
				subject = subject.capitalize()

	return {
		'prefix': prefix,  # TODO prefixes
		'subject': subject,
		'suffix': suffix  # TODO suffix.upper()
	}

def replace_teacher(text):
	"""Ersetzt einen Lehrer, entfernt Klammern"""
	if not text or text == '---':
		return None

	if text.startswith('(') and text.endswith(')'):
		text = text[1:-1]

	return text.capitalize()

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

def parse_response_date(date, logging=False):
	"""Parst das Datum für die Ajax Response"""
	date = datetime(**date)

	if logging:
		return date.strftime('%A, %d. %B %Y')

	else:
		return {
			'weekday': date.strftime('%A'),
			'date': date.strftime('%d. %B %Y')
		}
