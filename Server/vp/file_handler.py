import os
import shutil
import json
	
from .xml_reader import convert
from .exceptions import *

import logging

data_dir = os.path.join( os.path.dirname(__file__), 'data' )
json_file = os.path.join(data_dir, 'schedule.json')
tmp_file = os.path.join(data_dir, 'tmp.xml')
logfile = os.path.join(data_dir, 'server.log')

log = logging.getLogger('serverlog')
filehandler = logging.FileHandler(logfile)
console = logging.StreamHandler()

formatter = logging.Formatter(
	fmt='%(asctime)s [%(levelname)-8s] %(message)s',
	datefmt='%H:%M:%S'
)

log.setLevel(logging.DEBUG)
filehandler.setLevel(logging.DEBUG)

filehandler.setFormatter(formatter)
log.addHandler(filehandler)


def process_file(input_file):
	content = read_via_tmp(input_file)

	day = convert(content)

	try:
		with open(json_file, 'r+', encoding='utf-8') as fobj:
			old_data = json.loads( fobj.read() )
			data, action = add_day(old_data, day)

			content = json.dumps(data, ensure_ascii=False, indent=4, sort_keys=True)

			fobj.seek(0) # geht zum anfang der Datei
			fobj.write(content)
			fobj.truncate()

			log.info('%s file "%s" successfully', ('Added' if action == 'add' else 'Replaced'), day['filename'])
			return action

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
	try:
		days = data['days']
		for i, day in enumerate(days):
			if day['filename'] == new_day['filename']:
				days[i] = new_day # Überschreiben des schon vorhandenen Tages
				return data, 'replace'

		days.append(new_day) # Sonst hinzufügen als neuer Tag
		return data, 'add'

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