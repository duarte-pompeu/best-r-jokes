#!/usr/bin/python2

import praw
import sqlite3
import subprocess

# originally used to store secret keys
#~ import secrets

HIGH_SCORE = 1000
TWITTER_LIMIT = 140

# database
# open jokes_db
# create table submissions(id text, url text);

PATH_TO_DB = "home/jubileu/git/personal/best-r-jokes/jokes_db"
DB = sqlite3.connect("./jokes_db")
CURSOR = DB.cursor()

def id_in_db(post_id):
	CURSOR.execute("select id from submissions where id='%s'" % post_id)
	result =  CURSOR.fetchone()

	if result:
		return True
	else:
		return False


def save_in_db(post_id, post_url):
	CURSOR.execute("insert into submissions values('%s', '%s')" 
		% (post_id, post_url))


def get_url(post_id):
	return "https://www.reddit.com/r/Jokes/comments/" + post_id


def format_twitter_all(post_id, title, text):
	return "%s\n\n%s\n\n%s" %(title, text, get_url(post_id))


def format_twitter_title(post_id, title):
	return "%s\n\n%s" %(title, get_url(post_id))


def format_twitter_url(post_id):
	return "%s" % get_url(post_id)


def tweet(tweet_text):
	print "TWEETING: %s" % tweet_text
	subprocess.call(["twitter", "set", tweet_text])


def main():
	# https://praw.readthedocs.org/en/v3.0.0/pages/writing_a_bot.html#writing-a-bot
	r = praw.Reddit('PRAW related-question monitor by /u/_Daimon_ v 1.0. '
		'Url: https://praw.readthedocs.org/en/latest/'
		'pages/writing_a_bot.html')

	subreddit = r.get_subreddit('jokes')

	for submission in subreddit.get_hot(limit=10):
		title = submission.title
		post_id = submission.id
		score = submission.score

		if score < HIGH_SCORE:
			continue

		if id_in_db(post_id):
			continue
			#~ pass

		twitter_text = format_twitter_all(post_id, title, submission.selftext)

		if len(twitter_text) > TWITTER_LIMIT:
			continue
			
			# TODO: we can shorten tweets by using titles+urls/urls only
			#~ twitter_text = format_twitter_title(post_id, title)

		#~ if len(twitter_text) > TWITTER_LIMIT:
			#~ twitter_text = format_twitter_url(post_id)

		save_in_db(post_id, get_url(post_id))
		tweet(twitter_text)

	DB.commit()

if __name__ == "__main__":
	main()
