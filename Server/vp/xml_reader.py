import xml.etree.ElementTree as etree
import json

# TODO mal sehen, vllt brauche ich auch keine Klasse. Wird sich später zeigen.
class Event:
	"""
	Container-Klasse für ein Event
	Parsed das XML in das endgültige JSON in der schedule.json
	"""
	def __init__(self, element):
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

		self._class = get_text('klasse') # Syntax-Error vermieden
		self.time = get_text('stunde')
		self.subject = get_text('fach')
		self.teacher = get_text('lehrer')
		self.room = get_text('raum')
		self.info = get_text('info')

		# Liste aller vorgenommenen Änderungen
		self.changes = []
		if was_changed('fach'):
			self.changes.append('subject')

		if was_changed('lehrer'):
			self.changes.append('teacher')

		if was_changed('raum'):
			self.changes.append('room')

		if self.subject == '---':
			# löscht alle vorherigen changes, weil Ausfall als Info reicht.
			self.changes = ['canceled']

	def json(self):
		# Zufälligerweise entspricht die Struktur dieser Klasse exakt
		# dem benötigten json
		return json.dumps(self.__dict__)


def to_json(xml_content):
	root = etree.fromstring(xml_content)

	for action_elem in root.findall('./haupt/aktion'):
		event = Event(action_elem)
		

