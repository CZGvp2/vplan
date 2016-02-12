from pyramid.view import view_config
from .file_handler import get_schedule

@view_config(route_name='schedule', permission='read', renderer='templates/schedule.pt')
def schedule(request):
	return get_schedule()