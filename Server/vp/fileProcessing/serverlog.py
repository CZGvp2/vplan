import logging
import traceback
import os

from ..config import log_cfg

log = logging.getLogger('serverlog')
file_logger = logging.FileHandler(
	log_cfg['file'],
	mode=log_cfg['mode'],
	encoding='utf-8'
)

formatter = logging.Formatter(
	fmt=log_cfg['format'],
	datefmt=log_cfg['datefmt']
)

log.setLevel(log_cfg['level'])
file_logger.setLevel(log_cfg['level'])

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
