from pyramid.view import view_config

from datetime import datetime

from .fileProcessing.file_handler import read_schedule, to_datetime
from .fileProcessing.regex_parser import parse_response_date


@view_config(route_name='schedule', permission='read', renderer='templates/schedule.pt')
def schedule(request):
	data = read_schedule()
	data['from_upload'] = 'from_upload' in request.params

	for day in data['days']:
		day['date'] = parse_response_date(day['date'])

	return data


"""
Die Struktur vom Schedule Template Vars

--+
  |
  +-- from_upload [boolean]
  |
  +-- days [Array] (all die Tage)
      |
      +---+ (day)
      |   |
      |   +-- filename [String] (Name der Datei)
      |   |
      |   +-- date (Datum des Plans)
      |   |   |
      |   |   +-- weekday [String] (Wochentag)
      |   |   |
      |   |   +-- date [String] (Datum Bsp:"18. August 2012")
      |   |
      |   +-- events [Array]
      |       |
      |       +---+ (event)
      |       |   |
      |       |   +-- change [String] (die Veränderung: "SUBJECT" / "TEACHER" / "ROOM" / "CANCELLED" / "FAILED", letztes bei fehlparsen)
      |       |   |
      |       |   +-- time [Array] (Alle betreffenden Stundenzeiten)
	  |       |   |   |
	  |       |   |   +-- [int] (Stunde)
	  |       |   |   |
	  |       |   |  ...
      |       |   |
      |       |   +-- info [String] (None falls leer)
      |       |   |
      |       |   +-- selector [>> siehe weiter unten] (die Angesprochenen Klassen)
      |       |   |
      |       |   +-- targets [Array]
      |       |   |   |
      |       |   |   +-- [String] (ein Eintrag in Targets. z. B.: "9c", "11", "Mue")
      |       |   |   |
      |       |   |  ...
      |       |   |
      |       |   +-- old (alte Stunde)
      |       |   |   |
      |       |   |   +-- subject [String]
      |       |   |   |
      |       |   |   +-- teacher [String]
      |       |   |
      |       |   +-- new (Vertretungsstunde)
      |       |       |
      |       |       +-- subject [String]
      |       |       |
      |       |       +-- teacher [String]
      |       |       |
      |       |       +-- room [String] (alles None bei Ausfall)
      |       |
      |      ...
      |
     ...


>> siehe Hier

	for i, day in enumerate(data['days']):
		if to_datetime(day) == today:
			day_0 = i

		day['date'] = parse_response_date(day['date'])

	# Einfügen der relativen Indices mit day_0
	for i, day in enumerate(data['days']):
		day['index'] = i - day_0

"""
