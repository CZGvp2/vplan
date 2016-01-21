from pyramid.response import Response
from pyramid.security import remember, forget

from pyramid.httpexceptions import HTTPFound

from pyramid.view import view_config, view_defaults, notfound_view_config, forbidden_view_config

from .parser import process_file, get_schedule
from .group_finder import can_read, can_edit


@view_defaults(route_name='start', renderer='templates/login.pt')
class StartView:
	""" Startadresse "/". (Eigentlich Login) """ # <- Tim, das ist ein Python-Funktions-Docstring ;)
	def __init__(self, request):
		self.request = request

	def redirect(self, route_name, headers=None):
		# erspart Tipparbeit
		return HTTPFound(location=self.request.route_path(route_name), headers=headers)

	@view_config(request_method='GET')
	def view_start(self):
		"""Handelt einen GET-Request, wie z. B. Redirects"""

		# Falls in der URL der Query ?logout war, wird der User über forget abgemeldet, 
		# und zur Start(Anmelde)-Seite umgeleitet
		if 'logout' in self.request.params:
			headers = forget(self.request)
			return self.redirect('start', headers)
		
		# Redirects von der Startseite von schon angemeldeten Schülern
		if self.request.has_permission('read'):
			return self.redirect('schedule')
		
		if self.request.has_permission('edit'):
			return self.redirect('edit')

		# Falls keine der obigen Bedingungen erfüllt, kann es sich nur um eine
		# erstmalige Anmeldung handeln. Also noch nichts falsch angezeigt.
		return {'wrong_pwd':False}

	@view_config(request_method='POST')
	def answer_post(self):
		pwd_hash = self.request.params['hash']
		headers = None

		if can_read(pwd_hash):
			headers = remember(self.request, pwd_hash)
			return self.redirect('schedule', headers)

		if can_edit(pwd_hash):
			headers = remember(self.request, pwd_hash)
			return self.redirect('edit', headers)

		# wenn keines der obigen Bedingungen erfüllt, muss das Passwort
		# falsch gewesen sein.
		return {'wrong_pwd':True}


@view_defaults(route_name='edit', permission='edit', renderer='templates/edit.pt')
class EditView:
	def __init__(self, request):
		self.request = request

	@view_config(request_method='GET')
	def edit(self):
		return {'info': 'none'} # Dummy für nischt

	@view_config(request_method='POST')
	def upload(self):
		file_post = self.request.POST['file']
		if process_file(file_post):
			return {'info':'success'}

		return {'info':'error'}


@view_config(route_name='schedule', permission='read', renderer='templates/schedule.pt')
def schedule(request):
	return get_schedule()

@notfound_view_config(renderer='templates/error.pt')
def notfound(request):
	return {
		'title':'404 - nicht gefunden',
		'err_code':'404',
		'err_message':'Seite konnte nicht gefunden werden',
		'img_src':request.static_url('vp:static/img/404.jpg')
	}

@forbidden_view_config(renderer='templates/error.pt')
def forbidden(request):
	return {
		'title':'403 - kein Zugriff',
		'err_code':'403',
		'err_message':'Zugriff verweigert',
		'img_src':request.static_url('vp:static/img/403.jpg')
	}