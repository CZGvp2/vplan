import logging

from .file_handler import log_file


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