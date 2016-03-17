#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from time import sleep
import json
import random
from twython import Twython, TwythonError
import yaml

class GetRedditJokes():
	def __init__(self):
		# get twitter OAUTH keys
		with open('options.yaml', 'r') as f:
    			cred = yaml.load(f)

		self.twitter = Twython(cred["twitter"]["APP_KEY"],cred["twitter"]["APP_SECRET"],cred["twitter"]["OAUTH_TOKEN"],cred["twitter"]["OAUTH_TOKEN_SECRET"])

		# init reddit header
		self.hdr = { 'User-Agent' : 'super funny twitter bot by /u/jampola' }
		self.filename = 'jokes.json'

	def get_jokes(self):
		# get our jokes from /r/jokes (top, limit 10 and only past hour)
		jokes = requests.get("https://www.reddit.com/r/jokes/top.json", headers=self.hdr).json()

		# init a dict for us to store our jokes in
		joke_kv = dict()

		# count from 0, not using enumerate as it will skip numbers if a joke is over 140char
		c = 0
		for y in jokes['data']['children']:
			full_str="{}{}".format(y['data']['title'].encode('utf-8'),y['data']['selftext'].encode('utf-8'))
			if (len(full_str) < 140):
				joke_kv[c] = [y['data']['title'].encode('utf-8'),y['data']['selftext'].encode('utf-8')]
				c+=1
		
		# remove all data from file for good measure
		open(self.filename, 'w').close()

		# dump into our dictionary
		with open(self.filename, 'w') as fp:
			json.dump(joke_kv, fp)

	def prepare_jokes(self):
		# get our jokes from the json file
		with open(self.filename, 'r') as fp:
			read_data = json.load(fp)

			# get a count of how many jokes this hour
			length = len(read_data)
			count = 0

			# create a time period to sleep between each joke
			time_period = 3600 / length

			# iterate over the count of jokes in dict, if we reach the count....
			for x in range(0,length):
				# cleanly exit
				if count == length:
					exit()
				else:
					# pick a random index
					rand = random.sample(read_data, 1)[0]
					
					# build joke text
					joke = "{} {}".format(read_data[rand][0].encode('utf-8'),read_data[rand][1].encode('utf-8'))

					# tweet (and print) that shit
					self.twitter.update_status(status=joke)
					print joke

					# pop the joke from the the dict so we don't reuse it
					read_data.pop(rand)

					count += 1

					# sleep
					sleep(time_period)

	def run(self):
		self.get_jokes()
		self.prepare_jokes()
			
if __name__ == '__main__':
	app = GetRedditJokes()
	app.run()