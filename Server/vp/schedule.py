from pyramid.view import view_config
from .fileProcessing.file_handler import get_schedule


@view_config(route_name='schedule', permission='read', renderer='templates/schedule.pt')
def schedule(request):
	data = get_schedule()
	data['from_upload'] = 'from_upload' in request.params

	return data