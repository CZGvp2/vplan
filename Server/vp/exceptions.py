import sys
import logging
import traceback

log = logging.getLogger('serverlog')


class BasicError(Exception):
	def __init__(self, code, msg_format, log_level, **args):
		self.code = code
		self.format = msg_format
		self.log_level = log_level

		self.__dict__.update(args)

	def log(self):
		log.log(self.log_level, self.format % self.__dict__)


class ProcessingError(BasicError):
	"""Meldung die beim Bearbeiten eines Uploads entsteht, aber im schlimmsten Fall
	   einen Fehlschlag beim Hinzufügen einer Datei bedeuten"""

	def __init__(self, code, msg):
		msg = 'File "%(file)s": ' + msg
		BasicError.__init__(self, code, msg, logging.ERROR)


class BadEncodingError(ProcessingError):
	def __init__(self):
		ProcessingError.__init__(self, 'ERR_DECODING', 'Could not decode uploaded file')

class XMLParsingError(ProcessingError):
	def __init__(self, error):
		ProcessingError.__init__(self, 'ERR_PARSING_XML', 'XML Parsing Error at line %(line)d column %(column)d')
		self.line, self.column = error.position

class XMLReadingError(ProcessingError):
	def __init__(self, path):
		ProcessingError.__init__(self, 'ERR_READING_XML', 'Could not find tag or path "%(path)s"')
		self.path = path


class InternalServerError(BasicError):
	"""kritischer Fehler der auf eine dauerhafte Beeinträchtigung der Serverfunktionalität hinweist"""
	def __init__(self, msg):
		BasicError.__init__(self, 'INTERNAL_SERVER_ERROR', msg, logging.CRITICAL)


class IOServerError(InternalServerError):
	def __init__(self):
		InternalServerError.__init__(self, 'Could not load JSON file')

class JSONFileParsingError(InternalServerError):
	def __init__(self, error):
		InternalServerError.__init__(self, 'Parsing Error in JSON file line %(line)d column %(column)d')
		self.line = error.lineno
		self.column = error.colno

class JSONFileReadingError(InternalServerError):
	def __init__(self):
		InternalServerError.__init__(self, 'Invalid data structure in JSON file')


def log_unexpected_error():
	typ, msg, tb = sys.exc_info()
	log.critical('Unexpected Error\n%s\n%s', msg, traceback.format_tb(tb, limit=-1)[0])