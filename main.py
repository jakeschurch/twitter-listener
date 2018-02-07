#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import API
import json


class Listener(StreamListener):
    def __init__(self, start_time, time_limit):
        """ Initializer for Listener Class """
        self.time = start_time
        self.limit = time_limit
        self.tweet_counter = 0
        self.data = []

    def on_data(self, tweet):
        """ When data comes in, this appends the data and adds to counter """
        self.data.append(tweet)

        self.tweet_counter += 1
        print("{0} Tweet/s Downloaded".format(self.tweet_counter))

    def store_data(self):
        """ Writes data to JSON file """
        file.write(json.dumps(self.data))


def setup_auth(
        ckey='L5JVeOVkHIT0lE0hNHHF5ClVr',
        consumer_secret='rS4KyDgoz1MCRIeMVdwOqRD706S0cC5jCvxoYTsINbjWCZLl6f',
        access_token_key='958003558695276544-eUvZUiT2nRfiUWSZjpGGXjYJueh8Khh',
        access_token_secret='7ter6ZZGa9W7Vr3qBqfFwFB36sUQj8g7EQ9KneNJC5IaZ'):

    """ Sets up authentication for Twitter API """
    auth = OAuthHandler(ckey, consumer_secret)  # OAuth object
    auth.set_access_token(access_token_key, access_token_secret)

    return auth


def setup(jsonFile='twitterOutput.json', time_limit=30):
    """ Initializer for __main__ function """
    global file
    global auth
    global api
    global listener

    file = open(jsonFile, 'a')
    auth = setup_auth()
    api = API(auth)
    listener = Listener(time.time(), time_limit)


def get_tweet_stream(keywords: list):
    """ Opens connection with API for Stream Listener """

    # initialize Stream object with a time out limit
    twitterStream = Stream(auth, listener)
    twitterStream.filter(track=keywords, languages=['en'])


# def read_json_file(filename: str):
#     """ Read in a JSON file (issues with decoding Emojis so commented out) """
#     with open(filename, 'r') as f:
#         for l in f:
#             data = json.loads(l)
#             return data


def get_tweet_by_id(tweet_ID):
    """ Gets a specific tweet by ID """
    tweet = api.get_status(tweet_ID)
    file.write(json.dumps(tweet._json))


def get_tweets_by_user(screen_name):
    """ Gets most recent up to 200 (maximum allowed by API) tweets by user """
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    for tweet in new_tweets:
        file.write(json.dumps(tweet._json))


if __name__ == "__main__":
    """ Main Function """
    setup()
    try:
        # get_tweet_by_id(959393270144086016)
        # get_tweets_by_user('realDonaldTrump')
        get_tweet_stream(['Trump'])
    finally:
        listener.store_data()
        file.close()
