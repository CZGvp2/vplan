from pyramid.security import Deny, Allow, Everyone

class RootFactory:
	__acl__ = [
		(Allow, 'group:students', 'read'),
		(Allow, 'group:teachers', 'read'),
		(Allow, 'group:operator', 'edit')
	]

	def __init__(self, request):
		pass