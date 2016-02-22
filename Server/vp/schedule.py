from pyramid.view import view_config
from .fileProcessing.file_handler import read_schedule
from .fileProcessing.regex_parser import parse_response_date

@view_config(route_name='schedule', permission='read', renderer='templates/schedule.pt')
def schedule(request):
	data = read_schedule()
	data['from_upload'] = 'from_upload' in request.params

	for day in data['days']:
			day['date'] = parse_response_date(day['date'])

	return data