#!/usr/bin/env python2

import facebook
import secrets

def main():
	token = secrets.FB_TOKEN
	api = get_api(token)
	publish(api, "why did the chicken cross road? \n\n To get to the other side!", "www.example.org")

def get_api(access_token):
	graph = facebook.GraphAPI(access_token)
	return graph

def publish(api, joke, url):
	msg = joke + "\n\n" + url
	attachment = {
		"message" : msg,
	}
	#~ api.put_wall_post(" ", attachment=attachment)
	api.put_wall_post(msg)
	

if __name__ == "__main__":
	main()
