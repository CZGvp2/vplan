from pyramid.view import view_config, view_defaults, forbidden_view_config

import logging

from .file_handler import process_file
from .exceptions import ProcessingError, InternalServerError, log_unexpected_error


log = logging.getLogger('serverlog')

INTERNAL_ERROR = {
	'internalError': True,
	'sessionExpired': False,
	'results': None
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
		return dict()

	@view_config(request_method='POST', renderer='json')
	def upload(self):
		"""Bearbeitet den AJAX Post der Seite, gibt JSON zurück"""

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


def process_file_post(file_post):
	"""Bearbeitet einen einzelnen File-Post"""

	success = False
	filename = file_post.filename
	action = None
	date = None
	error_code = None

	try:
		action, date = process_file(file_post.file)
		success = True

		log.info('%s file "%s" (%s %s)', ('Added' if action == 'add' else 'Replaced'), filename, *date.values())

	except ProcessingError as error:
		error.file = filename
		error.log()

		error_code = error.code

	return {
		'success': success,
		'file': filename,
		'date': date,
		'action': action,
		'errorCode': error_code
	}

# 403 falls Session abgelaufen
@forbidden_view_config(accept='application/json', renderer='json')
def forbidden(request):
	return SESSION_EXPIRED


"""
Error Codes
- ERR_DECODING
- ERR_PARSING_XML
- ERR_READING_XML


Struktur der Response

--+
  |
  +-- internalError [boolean] (falls ein Server-Fehler auftrat, der nicht vom Nutzer beeinflusst werden kann)
  |
  +-- sessionExpired [boolean] (ob man noch angemeldet ist oder 403 bekommt)
  |
  +-- results [Array] (Ergebnisse der einzelnen Dateien, null falls Interner Fehler)
      |
      +---+ (Instanz des Arrays)
          |
          +-- success [boolean] (Falls Bearbeiten erfolgreich war)
          |
          +-- filename [String] (Name der Datei)
          |
          +-- date (Datum des Plans)
          |   |
          |   +-- weekday [String] (Wochentag)
          |   |
          |   +-- date [String] (Datum Bsp:"18. August 2012")
          |
          +-- errorCode [String] (Code des aufgetretenen Fehlers, bei keinem Fehler null)
          |
          +-- action [String] ('add' wenn Datei hinzugefügt, 'replace' wenn Datei ersetzt, null falls Fehler)


Beispiel

{
	"internalError": false,
	"sessionExpired": false,
	"results": [
		{
			"success": true,
			"filename": "VplanKl.xml",
			"date": {
				"weekday": "Montag",
				"date": "19. Oktober 2015"
			},
			"errorCode": null,
			"action": "add"
		},
		{
			"success": false,
			"filename": "VplanLe.xml",
			"errorCode": "ERR_READING_XML",
			"date": null,
			"action": null
		}
	]
}
"""