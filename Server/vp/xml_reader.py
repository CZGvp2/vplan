import xml.etree.ElementTree as etree

def to_json(xml_content):
	tree = etree.fromstring(xml_content)

	