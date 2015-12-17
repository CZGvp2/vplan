PASSWD = 'gunter'
PASSWD_EDIT = 'omg'

def get_group(passwd, request):
	if passwd == PASSWD:
		return ['group:students']

	elif passwd == PASSWD_EDIT:
		return ['group:editors']

	return []