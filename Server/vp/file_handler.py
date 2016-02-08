import os
import shutil
import json

from .xml_reader import convert

data_dir = os.path.join( os.path.dirname(__file__), 'data' )
json_file = os.path.join( data_dir, 'schedule.json')
tmp_file = os.path.join( data_dir, 'tmp.xml')

def read_via_tmp(input_file):
	with open(tmp_file, 'wb') as dest:
		shutil.copyfileobj(input_file, dest)

	try:
		with open(tmp_file, 'r') as fobj:
			content = fobj.read()

	except UnicodeDecodeError:
		return None

	finally:
		os.remove(tmp_file)

	return content

def process_file(file_post):
	if not hasattr(file_post, 'file'):
		return False

	input_file = file_post.file
	content = read_via_tmp(input_file)

	data = convert(content)
	
	if data is not None:
		with open(json_file, 'w') as fobj:
			raise Exception("Fehler!") # TODO make it work 
			return True

	return False

def get_schedule():
	with open(json_file, 'r', encoding='utf-8') as fobj:
		return eval(fobj.read())