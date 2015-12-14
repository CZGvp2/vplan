from pyramid.response import Response
from pyramid.security import remember, forget

from pyramid.httpexceptions import HTTPFound

from pyramid.view import view_config, view_defaults

from .login import PASSWD


@view_config(route_name='login', renderer='templates/login.pt')
def login(request):
	password = ''
	message = ''
	if 'form.submitted' in request.params:
		if request.params['password'] == PASSWD:

			headers = remember(request, 'hallo')
			return HTTPFound(location='/schedule', headers=headers)

		message = 'Falsch!'

	return dict(
		url=request.path,
		password='',
		message=message
	)

@view_config(route_name='schedule', permission='read')
def schedule(request):
	return Response('Eingeloggt.')



