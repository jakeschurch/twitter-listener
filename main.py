#!/usr/bin/env python3
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


def init(jsonFile='twitterOutput.json'):
    global file
    global auth
    global api

    file = open(jsonFile, 'a')
    auth = setup_auth()
    api = API(auth)


def get_tweet_stream(keywords: list, time_limit=30):
    start_time = time.time()

    # initialize Stream object with a time out limit
    twitterStream = Stream(auth, Listener(start_time, time_limit))
    twitterStream.filter(track=keywords, languages=['en'])


def read_json_file(filename: str):
    data = []
    for line in filename:
        data.append(json.loads(line))
    return data


def get_tweet_by_id(tweet_ID):
    tweet = api.get_status(tweet_ID)
    file.write('{0}\n'.format(json.dumps(tweet._json)))


def get_tweets_by_user(screen_name):
    # 200 is the maximum allowed count
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    for tweet in new_tweets:
        file.write('{0}\n'.format(json.dumps(tweet._json)))


if __name__ == "__main__":
    init()
    try:
        # get_tweet_by_id(959393270144086016)
        # get_tweets_by_user('realDonaldTrump')
        # get_tweet_stream(['python'])
    finally:
        file.close()
