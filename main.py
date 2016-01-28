#!/usr/bin/python2

import praw
import sqlite3
import subprocess

import config
import feed

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

def log(msg):
	if LOGGER:
		print msg

def id_in_db(post_id):
	CURSOR.execute("select id from submissions where id='%s'" % post_id)
	result =  CURSOR.fetchone()

	if result:
		return True
	else:
		return False


def save_in_db(post_id, post_url):
	sql = "insert into submissions values('%s', '%s')" \
		% (post_id, post_url)
	log("SQL: " + sql)
	CURSOR.execute(sql)


def get_url(post_id):
	return "redd.it/" + post_id


def format_twitter_all(post_id, title, text):
	return "%s\n\n%s\n\n%s" %(title, text, get_url(post_id))


def format_twitter_title(post_id, title):
	return "%s\n\n%s" %(title, get_url(post_id))


def format_twitter_url(post_id):
	return "%s" % get_url(post_id)


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


def main():
	# https://praw.readthedocs.org/en/v3.0.0/pages/writing_a_bot.html#writing-a-bot
	r = praw.Reddit('PRAW related-question monitor by /u/_Daimon_ v 1.0. '
		'Url: https://praw.readthedocs.org/en/latest/'
		'pages/writing_a_bot.html')

	subreddit = r.get_subreddit('jokes')

	feed.init()

	for submission in subreddit.get_hot(limit=20):
		title = submission.title
		post_id = submission.id
		score = submission.score
		text = submission.selftext

		log("%s : %d : %s ============" %(title, score, post_id))
		if score < HIGH_SCORE:
			log("score too low")
			continue

		if id_in_db(post_id):
			log("already in db")
			continue
			#~ pass

		twitter_text = format_twitter_all(post_id, title, submission.selftext)

		if len(twitter_text) < TWITTER_LIMIT:
			status = tweet(twitter_text)
			if status:
				save_in_db(post_id, get_url(post_id))

		else:
			log("text is too long for twitter: " + str(len(twitter_text)))

			if score >= LONG_TEXT_MIN_SCORE and not feed.item_in_feed("https://" + get_url(post_id)):
				result = feed.add_entry(title, "https://" + get_url(post_id), text)
				print result

	if not TESTING:
		DB.commit()

	result = feed.close()
	log(result)



if __name__ == "__main__":
	main()
