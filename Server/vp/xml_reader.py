import xml.etree.ElementTree as etree
import json

def to_json_event(self, element):
	# element ist das XML-Element-Objekt der jew. Aktion

	# liest den Tag 'tag' der Aktion
	get_text = lambda tag: element.find(tag).text

	# Name selbsterklärend, gibt eigentlich nur ein Dictionary zurück
	# In der XML-File werden Änderungen immer durch ein Attribut mit dem Wert "ae"
	# markiert. Sonst haben keine Tags in einer Aktion Attribute. Daher reicht es zu testen,
	# ob überhaupt Attribute vorliegen, also ob das attrib-dictionary etwas enthält.
	# Da nur in if's verwendet, reicht es, das dict zurückzugeben, da wenn len(dict) < 1, ist
	# dict als bool immer False, sonst True
	was_changed = lambda tag: element.find(tag).attrib

	# Liste aller vorgenommenen Änderungen
	changes = []
	if was_changed('fach'):
		changes.append('subject')

	if was_changed('lehrer'):
		changes.append('teacher')

	if was_changed('raum'):
		changes.append('room')

	if subject == '---':
		# löscht alle vorherigen changes, weil Ausfall als Info reicht.
		changes = ['cancelled']

	return {
		'class': get_text('klasse'),
		'time': get_text('stunde'),
		'subject': get_text('fach'),
		'teacher': get_text('lehrer'),
		'room': get_text('raum'),
		'info': get_text('info'),
		'changes': changes
	}

def to_json(xml_content):
	events = []
	root = etree.fromstring(xml_content)

	for action_elem in root.findall('./haupt/aktion'):
		event = to_json_event(action_elem)
		events.append(event)

	return json.dumps({'events':event})


		

