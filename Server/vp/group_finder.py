PASSWD_STD = 'gunter'
PASSWD_TCH = 'l3hr3r'
PASSWD_EDIT = 'omg'

def get_group(passwd, request):
	if passwd == PASSWD_STD:
		return ['group:students']

	elif passwd == PASSWD_TCH:
		return ['group:teachers']

	elif passwd == PASSWD_EDIT:
		return ['group:editors']

	return []