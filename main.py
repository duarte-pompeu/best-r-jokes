#!/usr/bin/python2

import praw
import sqlite3
import subprocess

# originally used to store secret keys
#~ import secrets


# set to true when testing without tweeting/commiting
LOGGER = False 
TESTING = False

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
	return "reddit.com/r/Jokes/" + post_id


def format_twitter_all(post_id, title, text):
	return "%s\n\n%s\n\n%s" %(title, text, get_url(post_id))


def format_twitter_title(post_id, title):
	return "%s\n\n%s" %(title, get_url(post_id))


def format_twitter_url(post_id):
	return "%s" % get_url(post_id)


def tweet(tweet_text):
	print ("TWEETING: " + tweet_text).encode('utf-8')
	
	if not TESTING:
		return subprocess.call(["/usr/local/bin/twitter", "set", tweet_text])
	
	else:
		return 0


def main():
	# https://praw.readthedocs.org/en/v3.0.0/pages/writing_a_bot.html#writing-a-bot
	r = praw.Reddit('PRAW related-question monitor by /u/_Daimon_ v 1.0. '
		'Url: https://praw.readthedocs.org/en/latest/'
		'pages/writing_a_bot.html')

	subreddit = r.get_subreddit('jokes')

	for submission in subreddit.get_hot(limit=20):
		title = submission.title
		post_id = submission.id
		score = submission.score
		
		log("%s : %d : %s ============" %(title, score, post_id))
		if score < HIGH_SCORE:
			log("score too low")
			continue

		if id_in_db(post_id):
			log("already in db")
			continue
			#~ pass

		twitter_text = format_twitter_all(post_id, title, submission.selftext)

		if len(twitter_text) > TWITTER_LIMIT:
			log("text is too long: " + str(len(twitter_text)))
			continue

		if tweet(twitter_text):
			save_in_db(post_id, get_url(post_id))

	if not TESTING:
		DB.commit()

if __name__ == "__main__":
	main()
