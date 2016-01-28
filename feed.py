#!/usr/bin/env python2

import xml.etree.ElementTree as ET
from email.Utils import formatdate

import config

TREE = None
CHANNEL = None

def init():
	global TREE, CHANNEL
	TREE = ET.parse(config.feed_path)
	root = TREE.getroot()
	CHANNEL = root.findall("channel")[0]


def close():
	trim_feed(config.max_feeds)
	TREE.write(config.feed_path)

	return ET.dump(TREE)


def item_in_feed(url):
	items = CHANNEL.findall("item")

	for item in items:
		link = item.find("link").text

		if link == url:
			return True


	else:
		return False


def add_entry(title, link, text):
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

	return  ET.dump(item)


def trim_feed(max_entries):
	entries = CHANNEL.findall("item")
	n_to_remove = len(entries) - max_entries

	for entry in entries[0:n_to_remove]:
		CHANNEL.remove(entry)

def get_time_stamp():
	return formatdate()

if __name__ == "__main__":
	main()

