#!/usr/bin/env python2

import xml.etree.ElementTree as ET
from email.Utils import formatdate

import config

CHANNEL = None
MAX_ENTRIES = 50

def main():

	tree = ET.parse(config.feed_path)
	root = tree.getroot()
	global CHANNEL
	CHANNEL = root.findall("channel")[0]
	
	item = ET.SubElement(CHANNEL, "item")
	a = ET.SubElement(item, "a")
	b = ET.SubElement(item, "b")
	
	add_new_entry("why did the chicken cross the road?", "https://www.example.com", "To get to the other side!")
	add_new_entry("why did the chicken cross the road?", "https://www.example.com", "To get to the other side!")
	add_new_entry("why did the chicken cross the road?", "https://www.example.com", "To get to the other side!")
	add_new_entry("why did the chicken cross the road?", "https://www.example.com", "To get to the other side!")
	add_new_entry("why did the chicken cross the road?", "https://www.example.com", "To get to the other side!")

	
	trim_tree(MAX_ENTRIES)
		
	ET.dump(root)
	tree.write(config.feed_path)

def add_new_entry(title, link, text):
	item = ET.SubElement(CHANNEL, "item")
	
	ti = ET.SubElement(item, "title")
	ti.text = title
	
	l = ET.SubElement(item, "link")
	l.text = link
	
	de = ET.SubElement(item, "description")
	te = "<p>" + text + "</p>"
	te += "<a href='" + link + "'>" + "View comments" + "</a>"
	
	de.text = te
	
	pd = ET.SubElement(item, "pubDate")
	pd.text = get_time_stamp()
	

def trim_tree(max_entries):
	entries = CHANNEL.findall("item")
	n_to_remove = len(entries) - max_entries
	
	for entry in entries[0:n_to_remove]:
		CHANNEL.remove(entry)

def get_time_stamp():
	return formatdate()
	
if __name__ == "__main__":
	main()

