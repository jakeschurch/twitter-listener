# Just starting setup

import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import os


ckey = 'L5JVeOVkHIT0lE0hNHHF5ClVr'
consumer_secret = 'rS4KyDgoz1MCRIeMVdwOqRD706S0cC5jCvxoYTsINbjWCZLl6f'
access_token_key = '958003558695276544-eUvZUiT2nRfiUWSZjpGGXjYJueh8Khh'
access_token_secret = '7ter6ZZGa9W7Vr3qBqfFwFB36sUQj8g7EQ9KneNJC5IaZ'

start_time = time.time() #grabs the system time
keyword_list = ['twitter'] #track list


#Listener Class Override
class listener(StreamListener):

	def __init__(self, start_time, time_limit=60):

		self.time = start_time
		self.limit = time_limit
		self.tweet_data = []

	def on_data(self, data):

		saveFile = io.open('raw_tweets.json', 'a', encoding='utf-8')

		while (time.time() - self.time) < self.limit:

			try:

				self.tweet_data.append(data)

				return True


			except BaseException, e:
				print 'failed ondata,', str(e)
				time.sleep(5)
				pass



auth = OAuthHandler(ckey, consumer_secret) #OAuth object
auth.set_access_token(access_token_key, access_token_secret)


twitterStream = Stream(auth, listener(start_time, time_limit=20)) #initialize Stream object with a time out limit
twitterStream.filter(track=keyword_list, languages=['en'])  #call the filter method to run the Stream Object
