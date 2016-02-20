import os
import shutil
import json

from .xml_reader import convert
from .regex_parser import parse_response_date
from .exceptions import *

data_dir = os.path.join( os.path.dirname(__file__), 'data' )
json_file = os.path.join(data_dir, 'schedule.json')
tmp_file = os.path.join(data_dir, 'tmp.xml')
log_file = os.path.join(data_dir, 'server.log')


def process_file(input_file):
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

	except IOError:
		raise IOServerError()

	except json.JSONDecodeError as error:
		raise JSONFileParsingError(error)

def read_via_tmp(input_file):
	with open(tmp_file, 'wb') as dest:
		shutil.copyfileobj(input_file, dest)

	try:
		with open(tmp_file, 'r', encoding='utf-8') as fobj:
			content = fobj.read()

	except UnicodeDecodeError:
		raise BadEncodingError()

	finally:
		os.remove(tmp_file)

	return content

def add_day(data, new_day):
	"""Fügt einen neuen Tag zu data hinzu. Gibt (data, info) zurück, wobei info (action, date) ist"""
	try:
		days = data['days']
		date = new_day['date']
		parsed_date = parse_response_date(date)

		for i, day in enumerate(days):
			if day['date'] == date:
				days[i] = new_day # Überschreiben des schon vorhandenen Tages
				return data, ('replace', parsed_date)

		days.append(new_day) # Sonst hinzufügen als neuer Tag
		return data, ('add', parsed_date)

	except KeyError as e:
		log.debug(e.args)
		raise JSONFileReadingError()

def get_schedule():
	try:
		with open(json_file, 'r', encoding='utf-8') as fobj:
			return json.loads(fobj.read())

	except IOError:
		log.error('Could not read JSON file: Error reading file')
		# TODO return error page

	except json.JSONDecodeError:
		log.error('Could not read JSON file: Error decoding JSON')
		# same