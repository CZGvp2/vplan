import os
import shutil

xml_dir = os.path.join( os.path.dirname(__file__), 'xml' )
xml_file = os.path.join( xml_dir, 'schedule.xml')
tmp_file = os.path.join( xml_dir, 'tmp.xml')

def read_via_tmp(input_file):
	with open(tmp_file, 'wb') as dest:
		shutil.copyfileobj(input_file, dest)

	with open(tmp_file, 'r') as fobj:
		content = fobj.read()

	os.remove(tmp_file)
	return content

def process_file(input_file):
	content = read_via_tmp(input_file)

	with open(xml_file, 'w') as fobj:
		fobj.write(content)