PASSWD = 'gunter'


def get_group(passwd, request):
	if PASSWD == 'gunter':
		return ['group:students']

	return []