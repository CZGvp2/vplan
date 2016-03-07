from pyramid.view import view_config, view_defaults, forbidden_view_config

from .fileProcessing.processing import process_file, remove_days, schedule
from .fileProcessing.regex_parser import parse_response_date
from .fileProcessing.serverlog import log, ProcessingError, InternalServerError, log_unexpected_error


INTERNAL_ERROR = {
	'internalError': True,
	'sessionExpired': False,
	'results': None,
}

SESSION_EXPIRED = {
	'internalError': False,
	'sessionExpired': True,
	'results': None
}


@view_defaults(route_name='upload', permission='upload')
class UploadView:
	"""Handler für die Upload-Seite"""
	def __init__(self, request):
		self.request = request

	@view_config(request_method='GET', renderer='templates/upload.pt')
	def view_site(self):
		"""Gibt die sichtbare Seite zurück"""
		with schedule(read_only=True, parse_date=True, no_events=True) as data:
			return data

	@view_config(request_method='POST', renderer='json')
	def handle_post(self):
		"""Bearbeitet den AJAX Post der Seite, gibt JSON zurück"""
		if 'delete' in self.request.params:
			return self.remove_files()

		else:
			return self.upload_files()

	def upload_files(self):
		"""Bearbeitet hochgeladene Dateien"""
		# Liste aller Ergebnisse der bearbeiteten Dateien
		results = []

		for file_post in self.request.POST.getall('file'):
			try:
				result = process_file_post(file_post)
				results.append(result)

			except InternalServerError as error:
				error.log()
				return INTERNAL_ERROR

			except:  # Anderer Fehler
				log_unexpected_error()
				return INTERNAL_ERROR

		return {
			'internalError': False,
			'sessionExpired': False,
			'results': results
		}

	def remove_files(self):
		"""Entfernt von Nutzer gelöschte Dateien"""
		filenames = self.request.POST.getall('delfile')
		remove_days(filenames)

def process_file_post(file_post):
	"""Bearbeitet einen einzelnen File-Post"""

	success = False
	filename = file_post.filename
	replaced = None
	date = None
	error_code = None

	try:
		process_file(file_post.file)
		success = True

	except ProcessingError as error:
		error.file = filename
		error.log()

		error_code = error.code

	return {
		'success': success,
		'file': filename,
		'date': date,
		'replaced': replaced,
		'errorCode': error_code
	}

# 403 falls Session abgelaufen
@forbidden_view_config(accept='application/json', renderer='json')
def forbidden(request):
	return SESSION_EXPIRED
