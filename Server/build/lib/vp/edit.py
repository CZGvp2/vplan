from pyramid.view import view_config, view_defaults

from .file_handler import process_file
from .exceptions import ProcessingError, InternalServerError, log_unexpected_error


@view_defaults(route_name='edit', permission='edit')
class EditView:
	def __init__(self, request):
		self.request = request

	@view_config(request_method='GET', renderer='templates/edit.pt')
	def view_edit(self):
		return dict()

	@view_config(request_method='POST', renderer='json')
	def upload(self):
		results = []

		for file_post in self.request.POST.getall('file'):
			try:
				action = process_file(file_post)
				result = {
					'success': True,
					'action': action
				}
				results.append(result)

			except ProcessingError as error:
				result = {
					'success': False,
					'errorCode': error.code
				}

				results.append(result)

			except InternalServerError as error:
				return {
					'internalError': True,
					'errorCode': error.code,
					'results': None
				}

			except: # Anderer Fehler
				log_unexpected_error()
				return {
					'internalError': True,
					'errorCode': 'UNEXPECTED'
				}

				
		return {
			'internalError': False,
			'results': results
		}