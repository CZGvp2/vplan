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

def can_read(passwd):
	return passwd in (PASSWD_STD, PASSWD_TCH)

def can_edit(passwd):
	return passwd == PASSWD_EDIT