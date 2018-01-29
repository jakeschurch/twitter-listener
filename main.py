#!/usr/bin/env python3
import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import io
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
time_limit = 30
keyword_list = ['python']  # track list
# params end


class Listener(StreamListener):
    def __init__(self, start_time, time_limit):

        self.time = start_time
        self.limit = time_limit
        self.tweet_data = []

    def on_data(self, data, fileName='rawTweets.json'):

        saveFile = io.open(fileName, 'a', encoding='utf-8')
        saveFile.write(data + '\n')

        # while (time.time() - self.time) < self.limit:
        #     self.tweet_data.append(data)
        #     return True

    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False


# setting up auth
auth = OAuthHandler(ckey, consumer_secret)  # OAuth object
auth.set_access_token(access_token_key, access_token_secret)

if __name__ == "__main__":
    twitterStream = Stream(auth, Listener(
        start_time,
        time_limit))  # initialize Stream object with a time out limit
    twitterStream.filter(
        track=keyword_list,
        languages=['en'])  # call the filter method to run the Stream Object
