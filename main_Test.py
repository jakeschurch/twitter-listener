#!/usr/bin/env python3
import time
import json
import tweepy
# import os
'''
TODO: func to grab tweets based off username
TODO: func to grab tweets based off hashtag
'''
# params start ---> DO NOT MODIFY KEYS!!!
ckey = 'L5JVeOVkHIT0lE0hNHHF5ClVr'
consumer_secret = 'rS4KyDgoz1MCRIeMVdwOqRD706S0cC5jCvxoYTsINbjWCZLl6f'
access_token_key = '958003558695276544-eUvZUiT2nRfiUWSZjpGGXjYJueh8Khh'
access_token_secret = '7ter6ZZGa9W7Vr3qBqfFwFB36sUQj8g7EQ9KneNJC5IaZ'

start_time = time.time()  # grabs the system time
time_limit = 120 # in seconds (will not terminate program but will stop printing tweets)
keyword_list = ['python']  # track list
# params end

# define listener class


class listener(tweepy.StreamListener):

    def __init__(self, start_time, time_limit):

        self.time = start_time
        self.limit = time_limit
        self.tweet_data = []

    def fix_data_string(self, x):   #turning JSON into dictionary (still have errors with some decoding)
        new_data = json.loads(x)
        return new_data

    def on_data(self, data):

        #saveFile = io.open('raw_tweets.json', 'a', encoding='utf-8')

        while (time.time() - self.time) < self.limit:

            print(data, " and ")
            newData = self.fix_data_string(data)
            print(newData["text"]) # getting text of tweet to check dictionary functionality
            print("")

            self.tweet_data.append(data)
            return True

    def on_status(self, status):
        print(status.text)

    def _initSaveFile(self, name='rawTweets.json'):
        with open(name) as f:
            pass
        f.close()

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False




# setting up auth
auth = tweepy.OAuthHandler(ckey, consumer_secret)  # OAuth object
auth.set_access_token(access_token_key, access_token_secret)

if __name__ == "__main__":
    #listener._initSaveFile()
    # pass
    twitterStream = tweepy.Stream(auth, listener(
        start_time,
        time_limit))  # initialize Stream object with a time out limit
    twitterStream.filter(
        track=keyword_list,
        languages=['en'])  # call the filter method to run the Stream Object
