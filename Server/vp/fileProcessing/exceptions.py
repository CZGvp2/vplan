import logging
import traceback

log = logging.getLogger('serverlog')


class BasicError(Exception):
	def __init__(self, msg_format, log_level, **args):
		self.format = msg_format
		self.log_level = log_level

		self.__dict__.update(args)

	def log(self):
		log.log(self.log_level, self.format % self.__dict__)


class ProcessingError(BasicError):
	"""Meldung die beim Bearbeiten eines Uploads entsteht, aber im schlimmsten Fall
	   einen Fehlschlag beim Hinzufügen einer Datei bedeuten"""

	def __init__(self, code, msg, **args):
		msg = 'File "%(file)s": ' + msg
		BasicError.__init__(self, msg, logging.ERROR, **args)
		self.code = code


class BadEncodingError(ProcessingError):
	def __init__(self):
		ProcessingError.__init__(self, 'ERR_DECODING', 'Could not decode uploaded file')

class XMLParsingError(ProcessingError):
	def __init__(self, error):
		line, col = error.position
		ProcessingError.__init__(self, 'ERR_PARSING_XML', 'XML Parsing Error at line %(line)d column %(column)d',
			line=line, column=col)

class XMLReadingError(ProcessingError):
	def __init__(self, path):
		ProcessingError.__init__(self, 'ERR_READING_XML', 'Could not find tag or path "%(path)s"', path=path)


class InternalServerError(BasicError):
	"""kritischer Fehler der auf eine dauerhafte Beeinträchtigung der Serverfunktionalität hinweist"""
	def __init__(self, msg, **args):
		BasicError.__init__(self, msg, logging.CRITICAL, **args)


class IOServerError(InternalServerError):
	def __init__(self, filename):
		InternalServerError.__init__(self, 'Could not load "%s"', filename=filename)

class JSONFileParsingError(InternalServerError):
	def __init__(self, error):
		InternalServerError.__init__(self, 'Parsing Error in JSON file line %(line)d column %(column)d',
			line=error.lineno, column=error.colno)

class JSONFileReadingError(InternalServerError):
	def __init__(self, error):
		InternalServerError.__init__(self, 'Invalid data structure in JSON') # TODO key


def log_unexpected_error():
	log.critical('Unexpected Error:\n' + traceback.format_exc(limit=-1))