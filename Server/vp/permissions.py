from pyramid.security import Deny, Allow, Everyone


class RootFactory:
	__acl__ = [
		(Allow, 'group:students', 'read'),
		(Allow, 'group:teachers', 'read'),
		(Allow, 'group:editors', 'read'),
		(Allow, 'group:editors', 'upload')
	]

	def __init__(self, request):
		self.request = request
