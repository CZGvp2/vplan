from pyramid.response import Response
from pyramid.security import remember, forget

from pyramid.httpexceptions import HTTPFound

from pyramid.view import view_config, view_defaults, notfound_view_config

import shutil
import os.path

from .login import PASSWD

upload_dir = 'C:/Users/Kamal/Desktop/vplan/Server/vp/uploads'

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

@view_config(route_name='schedule', permission='read')
def schedule(request):
	return Response('ge-schedult.')

@view_defaults(permission='edit')
class EditView:
	def __init__(self, request):
		self.request = request

	@view_config(route_name='edit', renderer='templates/edit.pt')
	def edit(self):
		return {}

	@view_config(route_name='upload')
	def upload(self):
		dest = os.path.normcase( os.path.join(upload_dir, 'test.txt') ) #TODO Timestamps
		with open(dest, 'wb') as dest_file:
			upload_file = self.request.POST['file'].file
			shutil.copyfileobj(upload_file, dest_file)

		return Response('ge-Uploaded.')
		

@notfound_view_config()
def notfound(request):
	return Response('Forbidden', status='404 Not Found')