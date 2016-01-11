from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from .group_finder import get_group
from .permissions import RootFactory

timeout = 60

def main(global_config, **settings):
	""" This function returns a Pyramid WSGI application.
	"""
	config = Configurator(settings=settings, root_factory=RootFactory)
	config.include('pyramid_chameleon')
	
	authn_policy = AuthTktAuthenticationPolicy(settings['vp.secret'], callback=get_group, hashalg='sha512', timeout=timeout)
	authz_policy = ACLAuthorizationPolicy()
	config.set_authentication_policy(authn_policy)
	config.set_authorization_policy(authz_policy)
	
	config.add_route('start', '/')
	config.add_route('edit', '/edit')
	config.add_route('schedule', '/schedule')

	config.add_static_view('static', 'static', cache_max_age=3600)
	config.scan()

	return config.make_wsgi_app()
