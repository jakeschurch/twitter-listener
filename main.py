#!/usr/bin/env python3
import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
'''
TODO: func to grab tweets based off username
TODO: Non-stream one quick pull
'''


class Listener(StreamListener):
    def __init__(self, start_time, time_limit):

        self.time = start_time
        self.limit = time_limit
        self.tweet_counter = 0

    def on_data(self, data):
        data = json.loads(data)

        global file
        file.write('{0}\n'.format(data))

        self.tweet_counter += 1
        print("{0} Tweet/s Downloaded".format(self.tweet_counter))


def setup_auth(
        ckey='L5JVeOVkHIT0lE0hNHHF5ClVr',
        consumer_secret='rS4KyDgoz1MCRIeMVdwOqRD706S0cC5jCvxoYTsINbjWCZLl6f',
        access_token_key='958003558695276544-eUvZUiT2nRfiUWSZjpGGXjYJueh8Khh',
        access_token_secret='7ter6ZZGa9W7Vr3qBqfFwFB36sUQj8g7EQ9KneNJC5IaZ'):
    auth = OAuthHandler(ckey, consumer_secret)  # OAuth object
    auth.set_access_token(access_token_key, access_token_secret)

    return auth


def init():
    file = open('rawJson.json', 'a')
    return file


def main(keyword_list: list, time_limit=30):
    start_time = time.time()

    # initialize Stream object with a time out limit
    twitterStream = Stream(setup_auth(), Listener(start_time, time_limit))
    twitterStream.filter(track=keyword_list, languages=['en'])


def read_json_file(filename: str):
    data = []
    for line in filename:
        data.append(json.loads(line))
    return data


if __name__ == "__main__":
    file = init()
    try:
        main(['python'])
    finally:
        file.close()
