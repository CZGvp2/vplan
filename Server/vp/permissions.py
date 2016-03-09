from pyramid.security import Deny, Allow, Everyone

from .config import logins


class RootFactory:
	__acl__ = [
		(Allow, 'group:readers', 'read'),
		(Allow, 'group:teachers', 'read'),
		(Allow, 'group:editors', 'read'),
		(Allow, 'group:editors', 'upload')
	]

	def __init__(self, request):
		self.request = request


def get_group(pwd_hash, request):
	if can_read(pwd_hash):
		return ['group:readers']

	elif can_edit(pwd_hash):
		return ['group:editors']

	return []

def can_read(pwd_hash):
	return pwd_hash == logins['reader']

def can_edit(pwd_hash):
	return pwd_hash == logins['editor']
