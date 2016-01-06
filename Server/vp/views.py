from pyramid.response import Response
from pyramid.security import remember, forget

from pyramid.httpexceptions import HTTPFound

from pyramid.view import view_config, view_defaults, notfound_view_config, forbidden_view_config

from .parser import process_file, get_schedule
from .group_finder import can_read, can_edit


@view_defaults(route_name='start', renderer='templates/login.pt')
class LoginView:
	def __init__(self, request):
		self.request = request

	def redirect(self, route_name, headers=None):
		return HTTPFound(location=self.request.route_path(route_name), headers=headers)

	@view_config(request_method='GET')
	def view_login(self):
		# wenn man angemeldet ist, sollte man auf der homepage direkt auf den plan weitergeleitet
		# werden. Aber dann kann man sich nicht nochmal anmelden, um zu editieren. Also kommt man
		# nicht um ein logout drumrum.

		if 'logout' in self.request.params:
			headers = forget(self.request)
			return self.redirect('start', headers)
		
		if self.request.has_permission('read'):
			return self.redirect('schedule')
		
		if self.request.has_permission('edit'):
			return self.redirect('edit')

		return {'wrong_pwd':False}

	@view_config(request_method='POST')
	def answer_post(self):
		password = self.request.params['password']
		headers = None

		if can_read(password):
			headers = remember(self.request, password)
			return self.redirect('schedule', headers)

		if can_edit(password):
			headers = remember(self.request, password)
			return self.redirect('edit', headers)

		return {'wrong_pwd':True}


@view_defaults(route_name='edit', permission='edit', renderer='templates/edit.pt')
class EditView:
	def __init__(self, request):
		self.request = request

	@view_config(request_method='GET')
	def edit(self):
		return {} # wird fuer response wichtig

	@view_config(request_method='POST')
	def upload(self):
		file_post = self.request.POST['file']

		process_file(file_post)

		return {}


@view_config(route_name='schedule', permission='read', renderer='templates/schedule.pt')
def schedule(request):
	return get_schedule()

@notfound_view_config(renderer='templates/error.pt')
def notfound(request):
	return {
		'title':'404 - nicht gefunden',
		'err_code':'404',
		'err_message':'Seite konnte nicht gefunden werden',
		'img_src':request.static_url('vp:static/img/404.png')
	}

@forbidden_view_config(renderer='templates/error.pt')
def forbidden(request):
	return {
		'title':'403 - kein Zugriff',
		'err_code':'403',
		'err_message':'Zugriff verweigert',
		'img_src':request.static_url('vp:static/img/403.png')
	}