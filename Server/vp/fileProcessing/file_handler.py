import os
import shutil
import json

from .serverlog import log, ProcessingError, InternalServerError
from .regex_parser import parse_response_date
from ..config import paths

SCHEDULE_STARTUP = {
	'days': []
}

class Schedule(object):
	"""Klasse zum Lesen und Schreiben der JSON File"""
	def __init__(self, read_only=False, parse_date=False, no_events=False):
		self.data = None
		self.fobj = None
		self.generated = False
		self.read_only = read_only
		self.parse_date = parse_date
		self.no_events = no_events


	def __enter__(self):
		"""Wird beim with-Statement aufgerufen"""
		try:
			self.fobj = open(paths['schedule'], 'r+', encoding='utf-8')
			self.data = json.loads( self.fobj.read() )

			for day in self.data['days']:
				if self.parse_date:
					day['date'] = parse_response_date(day['date'])

				if self.no_events:
					day.pop('events')

			return self.data

		except FileNotFoundError:
			log.warning('Schedule file not found. Generating new file.')
			self.generate_schedule()
			return self.data

		except json.JSONDecodeError as error:
			raise InternalServerError('Parsing Error in JSON file line %(line)d column %(column)d',
				line=error.lineno, column=error.colno)

	def __exit__(self, exc_type, exc_value, traceback):
		try:
			self.write()

		finally:
			self.fobj.close()

	def write(self):
		if not self.read_only or self.generated:
			content = json.dumps(self.data, ensure_ascii=False, indent=4, sort_keys=True)

			self.fobj.seek(0)  # geht zum anfang der Datei
			self.fobj.write(content)
			self.fobj.truncate()

	def generate_schedule(self):
		"""Erzeugt einen neuen leeren Schedule"""
		self.fobj = open(paths['schedule'], 'w', encoding='utf-8')
		self.data = SCHEDULE_STARTUP
		self.generated = True



def read_via_tmp(input_file):
	"""Liest die Daten einer Hochgeladenen Datei durch eine Temporärdatei"""
	with open(paths['tmp'], 'wb') as dest:
		shutil.copyfileobj(input_file, dest)

	try:
		with open(paths['tmp'], 'r', encoding='utf-8') as fobj:
			content = fobj.read()

	except UnicodeDecodeError:
		raise ProcessingError('ERR_DECODING', 'Bad Encoding')

	finally:
		os.remove(paths['tmp'])

	return content
