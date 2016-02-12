import sys
import logging
import traceback

log = logging.getLogger('serverlog')


class BasicError(Exception):
	def __init__(self, code, msg, args=None, log_level=logging.ERROR):
		self.code = code
		self.msg = msg
		self.args = args
		log.log(log_level, msg)


class ProcessingError(BasicError):
	"""Meldung die beim Bearbeiten eines Uploads entsteht, aber im schlimmsten Fall
	   einen Fehlschlag beim Hinzufügen einer Datei bedeuten"""

	def __init__(self, code, msg, **args):
		BasicError.__init__(self, code, msg, args, logging.ERROR)


class UnexpectedPostError(ProcessingError):
	def __init__(self):
		ProcessingError.__init__(self, 'ERR_READING_POST', 'Could not read POST data')

class BadEncodingError(ProcessingError):
	def __init__(self):
		ProcessingError.__init__(self, 'ERR_DECODING', 'Could not decode uploaded file')

class XMLParsingError(ProcessingError):
	def __init__(self, error):
		line, col = error.position
		msg = 'XML Parsing Error at line %d column %d' % error.position
		ProcessingError.__init__(self, 'ERR_PARSING_XML', msg, line=line, column=col)

class XMLReadingError(ProcessingError):
	def __init__(self, path):
		msg = 'Could not find tag or path "%s"' % path
		ProcessingError.__init__(self, 'ERR_READING_XML', msg, path=path)


class InternalServerError(BasicError):
	"""kritischer Fehler der auf eine dauerhafte Beeinträchtigung der Serverfunktionalität hinweist"""
	def __init__(self, msg, **args):
		BasicError.__init__(self, 'INTERNAL_SERVER_ERROR', msg, args, logging.CRITICAL)


class IOServerError(InternalServerError):
	def __init__(self):
		InternalServerError.__init__(self, 'Could not load JSON file')

class JSONFileParsingError(InternalServerError):
	def __init__(self, error):
		msg = 'Parsing Error in JSON file line %d column %d' % (error.lineno, error.colno)
		InternalServerError.__init__(self, msg)

class JSONFileReadingError(InternalServerError):
	def __init__(self):
		InternalServerError.__init__(self, 'Invalid data structure in JSON file')


def log_unexpected_error():
	typ, msg, tb = sys.exc_info()
	log.critical('Unexpected Error\n%s\n%s', msg, traceback.format_tb(tb, limit=-1)[0])