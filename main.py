#!/usr/bin/python2
# coding=utf-8

import praw
import sqlite3
import subprocess
import facebook #facebook-sdk from pip

import config
import feed
import secrets

# set to true when testing without tweeting/commiting
LOGGER = config.LOGGER
TESTING = config.TESTING

LONG_TEXT_MIN_SCORE = 1000
HIGH_SCORE = 500
TWITTER_LIMIT = 140

# database initialization
# sqlite> create table submissions(id text, url text);
DB = sqlite3.connect("./jokes_db")
CURSOR = DB.cursor()

def main():
	setup()
	# https://praw.readthedocs.org/en/v3.0.0/pages/writing_a_bot.html#writing-a-bot
	r = praw.Reddit('PRAW related-question monitor by /u/_Daimon_ v 1.0. '
		'Url: https://praw.readthedocs.org/en/latest/'
		'pages/writing_a_bot.html')

	subreddit = r.get_subreddit('jokes')

	feed.init()

	for submission in subreddit.get_hot(limit=20):
		analyze_and_post(submission)

	if not TESTING:
		DB.commit()

	feed.close()

def analyze_and_post(submission):
	title = submission.title
	post_id = submission.id
	score = submission.score
	text = submission.selftext

	log("%s : %d : %s" %(title, score, get_url(post_id)))
	if score < HIGH_SCORE:
		log("*** LOW SCORE ***")
		return

	if id_in_db(post_id):
		log("*** ALREADY IN DATABASE ***")
		return

	twitter_text = format_twitter_all(post_id, title, text)

	if config.POST_TO_TWITTER and len(twitter_text) < TWITTER_LIMIT :
		status = tweet(twitter_text)
		if status:
			save_in_db(post_id, get_url(post_id))

	else:
		url = get_long_url(post_id)
		https_url = "https://" + url
		if score >= LONG_TEXT_MIN_SCORE and not feed.item_in_feed(https_url):

			if config.POST_TO_RSS:
				feed.add_entry(title, https_url, text)
				print "NEW RSS FEED ===============\n" + title + " - " + https_url

			if config.POST_TO_FB:
				publish_facebook(title, text, url)
				print "NEW FACEBOOK POST ===============\n" + title + " - " + url


def tweet(tweet_text):
	text = tweet_text.encode('utf-8')
	print "TWEETING: " + text

	if not TESTING:
		try:
			return subprocess.call([config.twitter_path, "set", text])
		except Exception as e:
			print str(e)
			return 0
	else:
		return 0

def publish_facebook(title, text, url):
	token = secrets.FB_TOKEN
	api = facebook.GraphAPI(token)
	try:
		msg = title.encode("utf-8") + "\n\n" + text.encode("utf-8") + "\n\n" + url
		api.put_wall_post(msg)
	except Exception as e:
		print str(e)

	return


def id_in_db(post_id):
	CURSOR.execute("select id from submissions where id=?", [post_id])
	result =  CURSOR.fetchone()

	if result:
		return True
	else:
		return False


def save_in_db(post_id, post_url):
	sql = "insert into submissions values(?, ?)"
	log("SQL: " + sql + "\n" + post_id + ", " + post_url + "\n")
	CURSOR.execute(sql, [post_id, post_url])



def setup():
	import sys

	reload(sys)
	sys.setdefaultencoding('utf8')

def log(msg):
	if LOGGER:
		print msg


def get_long_url(post_id):
	return "reddit.com/r/jokes/" + post_id


def get_url(post_id):
	return "redd.it/" + post_id


def format_twitter_all(post_id, title, text):
	return "%s\n\n%s\n\n%s" %(title, text, get_url(post_id))


def format_twitter_title(post_id, title):
	return "%s\n\n%s" %(title, get_url(post_id))


def format_twitter_url(post_id):
	return "%s" % get_url(post_id)




if __name__ == "__main__":
	main()
