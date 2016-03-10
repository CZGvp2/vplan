from pyramid.view import view_config, notfound_view_config, forbidden_view_config
from .fileProcessing.serverlog import log_unexpected_error


@notfound_view_config(renderer='templates/error.pt')
def notfound(request):
	request.response.status = 404
	return {
		'title': '404 - nicht gefunden',
		'err_code': '404',
		'err_message': 'Seite konnte nicht gefunden werden',
		'img_src': request.static_path('vp:static/img/404.jpg')
	}

@forbidden_view_config(accept='text/html', renderer='templates/error.pt')
def forbidden(request):
	request.response.status = 403
	return {
		'title': '403 - kein Zugriff',
		'err_code': '403',
		'err_message': 'Zugriff verweigert',
		'img_src': request.static_path('vp:static/img/403.jpg')
	}

@view_config(context=Exception, renderer='templates/error.pt')
def internal_error(exc, request):
	log_unexpected_error()
	request.response.status = 500
	return {
		'title': '500 - Fehler',
		'err_code': '500',
		'err_message': 'Interner Fehler',
		'img_src': request.static_path('vp:static/img/500.jpg')
	}
