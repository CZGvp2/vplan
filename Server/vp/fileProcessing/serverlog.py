import logging
import traceback
import os


log_file = os.path.normpath( os.path.join( os.path.dirname(__file__), '../data/server.log' ) )

log = logging.getLogger('serverlog')
file_logger = logging.FileHandler(log_file)

formatter = logging.Formatter(
	fmt='%(asctime)s [%(levelname)-8s] %(message)s',
	datefmt='%H:%M:%S'
)

log.setLevel(logging.DEBUG)
file_logger.setLevel(logging.DEBUG)

file_logger.setFormatter(formatter)
log.addHandler(file_logger)


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
		self.file = 'unknown'


class InternalServerError(BasicError):
	"""kritischer Fehler der auf eine dauerhafte Beeinträchtigung der Serverfunktionalität hinweist"""
	def __init__(self, msg, **args):
		BasicError.__init__(self, msg, logging.CRITICAL, **args)


def log_unexpected_error():
	log.critical('Unexpected Error:\n' + traceback.format_exc(limit=-1))