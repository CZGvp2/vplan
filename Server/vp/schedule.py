from pyramid.view import view_config

from datetime import datetime

from .fileProcessing.file_handler import Schedule
from .fileProcessing.regex_parser import parse_response_date


@view_config(route_name='schedule', permission='read', renderer='templates/schedule.pt')
def view_schedule(request):
	"""Zeigt die sichtbare Seite an"""
	with Schedule(read_only=True, parse_date=True) as data:
		data['from_upload'] = 'from_upload' in request.params
		return data
