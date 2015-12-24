from pyramid.response import Response
from pyramid.security import remember, forget

from pyramid.httpexceptions import HTTPFound

from pyramid.view import view_config, view_defaults, notfound_view_config, forbidden_view_config

from .parser import process_file, get_schedule
from .group_finder import PASSWD_STD, PASSWD_EDIT


@view_defaults(route_name='login', renderer='templates/login.pt')
class LoginView:
	def __init__(self, request):
		self.request = request

	@view_config(request_method='GET')
	def view_login(self):
		if self.request.has_permission('read'):
			return HTTPFound(location='/schedule')

		if self.request.has_permission('edit'):
			return HTTPFound(location='/edit')

		return {'action':self.request.path}

	@view_config(request_method='POST')
	def answer_post(self):
		password = self.request.params['password']
		headers = None

		if password == PASSWD_STD:
			headers = remember(self.request, password)
			location = '/schedule'

		elif password == PASSWD_EDIT:
			headers = remember(self.request, password)
			location = '/edit'

		else:
			location = '/'
			headers = None

		return HTTPFound(location=location, headers=headers)


@view_defaults(route_name='edit', permission='edit', renderer='templates/edit.pt')
class EditView:
	def __init__(self, request):
		self.request = request

	@view_config(request_method='GET')
	def edit(self):
		return {'action':self.request.path}

	@view_config(request_method='POST')
	def upload(self):
		file_post = self.request.POST['file']

		process_file(file_post)

		return {'action':self.request.path}


@view_config(route_name='schedule', permission='read', renderer='templates/schedule.pt')
def schedule(request):
	return get_schedule()

@notfound_view_config()
def notfound(request):
	return Response('Gibts nich.', status='404 Not Found')

@forbidden_view_config(renderer='templates/error.pt')
def forbidden(request):
	return {
		'title':'403 - kein Zugriff',
		'err_code':'403',
		'err_message':'Zugriff verweigert',
		'img_src':request.static_url('vp:static/img/403.png')
	}