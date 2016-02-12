from pyramid.view import notfound_view_config, forbidden_view_config

@notfound_view_config(renderer='templates/error.pt')
def notfound(request):
	return {
		'title': '404 - nicht gefunden',
		'err_code': '404',
		'err_message': 'Seite konnte nicht gefunden werden',
		'img_src': request.static_url('vp:static/img/404.jpg')
	}

@forbidden_view_config(renderer='templates/error.pt')
def forbidden(request):
	return {
		'title': '403 - kein Zugriff',
		'err_code': '403',
		'err_message': 'Zugriff verweigert',
		'img_src': request.static_url('vp:static/img/403.jpg')
	}