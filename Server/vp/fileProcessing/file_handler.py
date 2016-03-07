import os
import shutil
import json

from .serverlog import log, ProcessingError, InternalServerError
from .regex_parser import parse_response_date


data_dir = os.path.normpath( os.path.join( os.path.dirname(__file__), '../data' ) )
json_file = os.path.join(data_dir, 'schedule.json')
tmp_file = os.path.join(data_dir, 'tmp.xml')

SCHEDULE_STARTUP = {
	'days': []
}

class JSONFile(object):
	"""Klasse zum Lesen und Schreiben der JSON File"""
	def __init__(self):
		self.data = None
		self.fobj = None
		self.read_only = False
		self.parse_date = False
		self.no_events = False

	def __call__(self, read_only=False, parse_date=False, no_events=False):
		"""Funktion die Instanz zurückgibt, zum Parameter-Bearbeiten"""
		self.read_only = read_only  # Überschreibt die schedule.json nicht
		self.parse_date = parse_date  # Ersetzt die Systemdaten durch Wochentag und Datum
		self.no_events = no_events  # Entfernt alle events (nur Dateinamen und Datum)

		return self

	def __enter__(self):
		"""Wird beim with-Statement aufgerufen"""
		try:
			self.fobj = open(json_file, 'r+', encoding='utf-8')
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
		if not self.read_only:
			content = json.dumps(self.data, ensure_ascii=False, indent=4, sort_keys=True)

			self.fobj.seek(0)  # geht zum anfang der Datei
			self.fobj.write(content)
			self.fobj.truncate()

	def generate_schedule(self):
		"""Erzeugt einen neuen leeren Schedule"""
		self.fobj = open(json_file, 'w', encoding='utf-8')
		self.data = SCHEDULE_STARTUP

		self.write()


def read_via_tmp(input_file):
	"""Liest die Daten einer Hochgeladenen Datei durch eine Temporärdatei"""
	with open(tmp_file, 'wb') as dest:
		shutil.copyfileobj(input_file, dest)

	try:
		with open(tmp_file, 'r', encoding='utf-8') as fobj:
			content = fobj.read()

	except UnicodeDecodeError:
		raise ProcessingError('ERR_DECODING', 'Bad Encoding')

	finally:
		os.remove(tmp_file)

	return content
