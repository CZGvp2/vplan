import xml.etree.ElementTree as etree

class Action:
	def __init__(self, element):
		get_text = lambda tag: element.find(tag).text

		self.class2 = get_text('class') # class -> Syntax Error, Ich musste den Server irgendwie zum Starten kriegen
		self.time = get_text('stunde')
		self.subject = get_text('fach')
		self.teacher = get_text('lehrer')  # TODO attribute für Änderung
		self.room = get_text('raum')
		self.info = get_text('info')

def to_json(xml_content):
	root = etree.fromstring(xml_content)

	for action in root.findall('./haupt/aktion'):
		print(action.find('klasse').text)

#with open('VplanKl.xml') as fobj:
#	to_json(fobj.read())
#		open(...) -> No such file or directory...
input()