PASSWD_STD = '4c1697f84dc5330cbafd5f55ff553b35654381b4fc448ed8b03b9c814aa88d2b6329b9310db202b1a058ba546008cee3d37e2165245016ee44cb43aab5febbf3'
PASSWD_TCH = '3546bf7317ab4ae486f818c39f357c79559f8e73f3de2243ff449d48ae4992bb4ffb0a17e46dde8e17e48e81c4264f54e9bd705991c673eeb4e293ccf900f021'
PASSWD_EDIT = 'a1eb442d3b6c9680e95b73033968223e6ea5fbff7c3d6ed8f6f9ec38cec74cad307f5b8662291323c65e81cc2ec1d24384e4c1a165aed36d9874efecf976b2c4'


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