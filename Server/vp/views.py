from pyramid.response import Response
from pyramid.security import remember, forget

from pyramid.httpexceptions import HTTPFound

from pyramid.view import view_config, view_defaults, notfound_view_config, forbidden_view_config

from .parser import process_file
from .group_finder import PASSWD

@view_config(route_name='login', renderer='templates/login.pt')
def login(request):
	message = ''
	if 'form.submitted' in request.params:
		password = request.params['password']
		if password == PASSWD:
			headers = remember(request, password)
			return HTTPFound(location='/schedule', headers=headers)

		elif password == 'omg':
			headers = remember(request, password)
			return HTTPFound(location='/edit', headers=headers)

		message = 'Falsch!'

	return dict(
		url=request.path,
		password='',
		message=message
	)

@view_config(route_name='schedule', permission='read', renderer='templates/schedule.pt')
def schedule(request):
	return {}

@view_defaults(permission='edit')
class EditView:
	def __init__(self, request):
		self.request = request

	@view_config(route_name='edit', renderer='templates/edit.pt')
	def edit(self):
		return {}

	@view_config(route_name='upload')
	def upload(self):
		upload_file = self.request.POST['file'].file

		process_file(upload_file)

		return Response('ge-Uploaded.')
		

@notfound_view_config()
def notfound(request):
	return Response('Gibts nich.', status='404 Not Found')

@forbidden_view_config()
def forbidden(request):
	return Response('Darfst du nich.', status='403 Forbidden')