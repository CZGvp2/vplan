import os
import shutil
import json
	
from .xml_reader import convert

import logging


data_dir = os.path.join( os.path.dirname(__file__), 'data' )
json_file = os.path.join( data_dir, 'schedule.json')
tmp_file = os.path.join( data_dir, 'tmp.xml')
logfile = os.path.join( data_dir, 'server.log')


log = logging.getLogger('serverlog')
filehandler = logging.FileHandler(logfile)
console = logging.StreamHandler()

formatter = logging.Formatter(
	fmt='%(asctime)s %(module)s:%(funcName)s [%(levelname)s] %(message)s',
	datefmt='%H:%M:%S'
)

log.setLevel(logging.DEBUG)
filehandler.setLevel(logging.DEBUG)

filehandler.setFormatter(formatter)
log.addHandler(filehandler)


def read_via_tmp(input_file):
	with open(tmp_file, 'wb') as dest:
		shutil.copyfileobj(input_file, dest)

	try:
		with open(tmp_file, 'r', encoding='utf-8') as fobj:
			content = fobj.read()

	except UnicodeDecodeError:
		log.error('Could not decode uploaded file')
		return None

	finally:
		os.remove(tmp_file)

	return content

def process_file(file_post):
	if not hasattr(file_post, 'file'):
		return False

	input_file = file_post.file
	content = read_via_tmp(input_file)

	day = convert(content)
	
	if day is None:
		return False

	try:
		with open(json_file, 'r+', encoding='utf-8') as fobj:
			data = json.loads( fobj.read() )

			data = add_day(data, day)

			if not data:
				# Fehler beim Hinzufügen
				return False

			content = json.dumps(data, ensure_ascii=False, indent=4, sort_keys=True)

			fobj.seek(0) # geht zum anfang der Datei
			fobj.write(content)
			fobj.truncate()

			log.info('Uploaded File "%s" successfully', day['filename'])
			return True

	except IOError:
		log.error('Could not write into JSON file')
		return False

	except json.JSONDecodeError as e:
		log.error('Parsing Error in JSON file line %d column %d', e.lineno, e.colno)
		return False

def add_day(data, new_day):
	try:
		days = data['days']
		for i, day in enumerate(days):
			if day['filename'] == new_day['filename']:
				days[i] = new_day # Überschreiben des schon vorhandenen Tages
				return data

		days.append(new_day) # Sonst hinzufügen als neuer Tag
		return data

	except KeyError:
		log.error('Invalid data structure in JSON file')
		return None

def get_schedule():
	try:
		with open(json_file, 'r', encoding='utf-8') as fobj:
			return json.loads(fobj.read())

	except IOError:
		log.error('Could not read JSON file: Error reading file')
		# TODO return error page

	except json.JSONDecodeError: # läuft nur auf Python 3.5 !!! (ja ist notwendig)
		log.error('Could not read JSON file: Error decoding JSON')
		# same