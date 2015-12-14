from pyramid.response import Response
from pyramid.security import remember, forget

from pyramid.httpexceptions import HTTPFound

from pyramid.view import view_config, view_defaults, notfound_view_config

from .login import PASSWD

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
	return HTTPFound(location='/schedule', headers=headers)

@view_config(route_name='edit', permission='edit')
def edit(request):
	return Response('edittet.')

@notfound_view_config()
def notfound(request):
    return Response('<center style="margin-top:10em;"><b style="text-transform:uppercase;font-family:monospace;letter-spacing:1em;"><h2>404:</h2> Der Fehler 404 konnte nicht gefunden werden.</b></center>', status='404 Not Found')