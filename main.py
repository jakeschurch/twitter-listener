#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import API, api
import json


class Listener(StreamListener):
    def __init__(self, start_time, time_limit):

        self.time = start_time
        self.limit = time_limit
        self.tweet_counter = 0
        self.data = []

    def on_data(self, tweet):

        self.data.append(tweet)

        self.tweet_counter += 1
        print("{0} Tweet/s Downloaded".format(self.tweet_counter))

    def store_data(self):
        file.write(json.dumps(self.data))


def setup_auth(
        ckey='L5JVeOVkHIT0lE0hNHHF5ClVr',
        consumer_secret='rS4KyDgoz1MCRIeMVdwOqRD706S0cC5jCvxoYTsINbjWCZLl6f',
        access_token_key='958003558695276544-eUvZUiT2nRfiUWSZjpGGXjYJueh8Khh',
        access_token_secret='7ter6ZZGa9W7Vr3qBqfFwFB36sUQj8g7EQ9KneNJC5IaZ'):

    auth = OAuthHandler(ckey, consumer_secret)  # OAuth object
    auth.set_access_token(access_token_key, access_token_secret)

    return auth


def init(jsonFile='twitterOutput.json', time_limit=30):
    global file
    global auth
    global api
    global listener

    file = open(jsonFile, 'a')
    auth = setup_auth()
    api = API(auth)
    listener = Listener(time.time(), time_limit)


def get_tweet_stream(keywords: list):

    # initialize Stream object with a time out limit
    twitterStream = Stream(auth, listener)
    twitterStream.filter(track=keywords, languages=['en'])


def read_json(filename: str):

    with open(filename, 'r') as f:
        for line in f:
            data = json.loads(line)

        data = [json.loads(d) for d in data]
        return data


def get_tweet_by_id(tweet_ID):
    tweet = api.get_status(tweet_ID)
    file.write(json.dumps(tweet._json))


def get_tweets_by_user(screen_name):
    # 200 is the maximum allowed count
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    for tweet in new_tweets:
        file.write(json.dumps(tweet._json))

def testing():
    """
    [Attributes]
        created_at
        id -> tweet
        text

    [Nested] -> user
        id
        screen name
        location
    """
    vals = read_json('twitterOutput.json')

    for val in vals:
        for v in vals:
            print(v)


def load_json(filename: str):
    data = read_json(filename)
    for d in data:
        try:
            if d["truncated"] == "true":
                pass
        except KeyError:
            print(d)


if __name__ == "__main__":
    init()
    # testing()
    load_json('twitterOutput.json')
    # try:
    #     # get_tweet_by_id(959393270144086016)
    #     # get_tweets_by_user('realDonaldTrump')
    #     get_tweet_stream(['Trump'])
    # finally:
    #     listener.store_data()
    #     file.close()
