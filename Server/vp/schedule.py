from pyramid.view import view_config

from datetime import datetime

from .fileProcessing.file_handler import read_schedule, to_datetime
from .fileProcessing.regex_parser import parse_response_date

@view_config(route_name='schedule', permission='read', renderer='templates/schedule.pt')
def schedule(request):
	data = read_schedule()
	data['from_upload'] = 'from_upload' in request.params

	today = datetime.today().date()
	day_0 = 0  # Heute

	for i, day in enumerate(data['days']):
		if to_datetime(day) == today:
			day_0 = i

		day['date'] = parse_response_date(day['date'])

	# Einfügen der relativen Indices mit day_0
	for i, day in enumerate(data['days']):
		day['index'] = i - day_0

	return data