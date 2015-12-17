import os
import shutil

xml_dir = os.path.join( os.path.dirname(__file__), 'xml' )
xml_file = os.path.join( xml_dir, 'schedule.xml')
tmp_file = os.path.join( xml_dir, 'tmp.xml')

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

	if content is not None:
		with open(xml_file, 'w') as fobj:
			fobj.write(content)

		return True

	return False