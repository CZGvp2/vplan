from datetime import datetime

from .file_handler import read_via_tmp, JSONFile
from .xml_reader import convert
from .regex_parser import parse_response_date
from .serverlog import log

schedule = JSONFile()

to_datetime = lambda day: datetime(**day['date'])

def process_file(input_file):
	"""Bearbeitet eine einzelne Datei"""
	# Lesen der Daten mit Temporärdatei
	content = read_via_tmp(input_file)

	# Konvertieren von XML zu JSON
	new_day = convert(content)

	with schedule() as data:
		# Hinzufügen des Tages zu den Daten
		days = data['days']
		new_date = new_day['date']

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

		log.info('%s day %s', ('Replaced' if replaced else 'Added'), parse_response_date(new_date, logging=True))

def remove_days(filenames):
	with schedule() as data:
		# Hinzufügen des Tages zu den Daten
		for i, day in enumerate( data['days'].copy() ):
			if day['filename'] in filenames:
				data['days'].pop(i)
				log.info('Removed day %s', parse_response_date(day['date'], logging=True))
