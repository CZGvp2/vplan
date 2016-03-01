import os
import shutil
import json
from datetime import datetime

from .xml_reader import convert
from .regex_parser import parse_response_date
from .serverlog import log, ProcessingError, InternalServerError


data_dir = os.path.normpath( os.path.join( os.path.dirname(__file__), '../data' ) )
json_file = os.path.join(data_dir, 'schedule.json')
tmp_file = os.path.join(data_dir, 'tmp.xml')
log_file = os.path.join(data_dir, 'server.log')

SCHEDULE_STARTUP = {
	'days': []
}


def process_file(input_file):
	"""Bearbeitet eine einzelne Datei"""
	# Lesen der Daten mit Temporärdatei
	content = read_via_tmp(input_file)

	# Konvertieren von XML zu JSON
	day = convert(content)

	try:
		with open(json_file, 'r+', encoding='utf-8') as fobj:
			# Laden der alten Daten
			old_data = json.loads( fobj.read() )

			# Hinzufügen des Tages zu den Daten
			data, info = add_day(old_data, day)

			# Speichern der neuen Daten
			content = json.dumps(data, ensure_ascii=False, indent=4, sort_keys=True)

			fobj.seek(0) # geht zum anfang der Datei
			fobj.write(content)
			fobj.truncate()

			return info

	except FileNotFoundError:
		generate_schedule()

	except json.JSONDecodeError as error:
		raise InternalServerError('Parsing Error in JSON file line %(line)d column %(column)d',
			line=error.lineno, column=error.colno)

def read_via_tmp(input_file):
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

to_datetime = lambda day: datetime(**day['date'])

def add_day(data, new_day):
	"""Fügt einen neuen Tag zu data hinzu. Gibt (data, info) zurück, wobei info (action, date) ist"""
	try:
		days = data['days']
		new_date = new_day['date']
		parsed_date = parse_response_date(new_date)

		# Entfernen veralteter Dateien (erstmal nich)
#		today = datetime.today()
#		for day in days.copy():
#			date = to_datetime(day)
#			if date < today.date():
#				days.remove(day)
#				log.info('Removed day %s', date.strftime('%A %d. %B %Y'))
#
#			else:
#				break

		# Einfügen des Tages
		replaced = False
		for i, day in enumerate(days):
			if day['date'] == new_date:
				days[i] = new_day # Überschreiben des schon vorhandenen Tages
				replaced = True
				break

		if not replaced:
			days.append(new_day) # Sonst hinzufügen als neuer Tag

		# Sortieren nach Datum
		days.sort(key=to_datetime)

		return data, (replaced, parsed_date)

	except KeyError as error:
		raise InternalServerError('Error reading json. Could not find key "%(key)s"', key=error.args[0])

def read_schedule():
	"""Gibt die Daten aus schedule als dict zurück"""
	try:
		with open(json_file, 'r', encoding='utf-8') as fobj:
			return json.loads(fobj.read())

	except FileNotFoundError:
		generate_schedule()
		return SCHEDULE_STARTUP

	except json.JSONDecodeError as error:
		raise InternalServerError('Parsing Error in JSON file line %(line)d column %(column)d',
			line=error.lineno, column=error.colno)

def generate_schedule():
	"""Erzeugt einen neuen leeren Schedule"""

	log.warning('schedule.json not found. Generating new file.')
	with open(json_file, 'w', encoding='utf-8') as fobj:
		content = json.dumps(SCHEDULE_STARTUP, ensure_ascii=False, indent=4, sort_keys=True)
		fobj.write(content)
