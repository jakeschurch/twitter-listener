#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import API

import simplejson as json
import csv
import keys  # python file that holds my secret key


class Listener(StreamListener):
    def __init__(self, time_limit, tweet_limit=1):
        """ Initializer for Listener Class """
        self.time = time.time.now()
        self.limit = time_limit
        self.tweet_counter = 0
        self.tweet_limit = tweet_limit
        self.data = []
        self.StreamObj = None

    def on_data(self, tweet):
        """ When data comes in, this appends the data and adds to counter """
        if self.tweet_counter <= self.tweet_limit:
            self.data.append(tweet)

            self.tweet_counter += 1
            print("{0} Tweet/s Downloaded".format(self.tweet_counter))
        else:
            self.StreamObj.disconnect()
            results.extend(self.data[:-1])


class tweet():
    def __init__(self, tweetId, createdAt, text, userId):
        self.tweetId = tweetId
        self.createdAt = createdAt
        self.text = text
        self.userId = userId

    def to_record(self) -> list:
        return [self.tweetId, self.createdAt, self.text, self.userId]


def get_tweet_by_id(tweet_ID, api):
    """ Gets a specific tweet by ID """
    tweet = api.get_status(tweet_ID)
    results.extend(tweet._json)


def get_tweets_by_user(screen_name, api, count=200):
    """ Gets most recent up to 200 (maximum allowed by API) tweets by user """

    new_tweets = api.user_timeline(screen_name=screen_name, count=count)
    objs = [(x._json) for x in new_tweets]
    results.extend(objs)
        # results.extend(
        #     tweet(
        #         tweetId=item['id_str'],
        #         createdAt=item['created_at'],
        #         text=item['text'],
        #         userId=item['user']['screen_name']))


def to_csv(tweet_list: list, file_name='tweet_output.csv', delim=','):
    with open(file_name, "a") as file:
        csv_writer = csv.writer(file, delimiter=delim)

        # write headers to file
        csv_writer.writerow(['tweetId', 'createdAt', 'text', 'userId'])
        for tweet_value in tweet_list:
            csv_writer.writerow(tweet_value.__dict__.values())


def write_json(data: list, file, overwrite: str):
    if overwrite is True:
        filemode = 'w'
    else:
        filemode = 'a'
    with open(file, filemode) as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ': '))


def read_json(file: str):
    with open(file, 'r') as f:
        for line in f:
            data = json.loads(line, encoding='utf8')
    return data


def get_tweet_stream(keywords: list, auth, listener: Listener):
    """ Opens connection with API for Stream Listener """
    twitterStream = Stream(auth, listener)
    listener.StreamObj = twitterStream
    twitterStream.filter(track=keywords, languages=['en'])


def setup_auth():
    """ Sets up authentication for Twitter API """
    ckey, consumer_secret, access_token_key, access_token_secret = keys.GetSecrets(
    )
    auth = OAuthHandler(ckey, consumer_secret)  # OAuth object
    auth.set_access_token(access_token_key, access_token_secret)

    api = API(auth)
    return auth, api


def to_tweets(jsonList):
    tweets = []
    for item in jsonList:
        tweets.append(
            tweet(
                tweetId=item['id_str'],
                createdAt=item['created_at'],
                text=item['text'],
                userId=item['user']['screen_name']))
    return tweets


def main(keywords: list,
         filename: str,
         byId=False,
         byUser=False,
         byStream=False,
         timeLimit=None,
         tweetLimit=50,
         overwrite=False):
    global results
    results = []

    auth, api = setup_auth()

    if byStream is True:
        listener = Listener(timeLimit, tweetLimit)
        get_tweet_stream(keywords, listener)
    if byId is True:
        for kw in keywords:
            get_tweet_by_id(kw, api)
    if byUser is True:
        for kw in keywords:
            get_tweets_by_user(kw, api, tweetLimit)

    write_json(results, filename, overwrite)
    jsonTweets = read_json(filename)

    tweets = to_tweets(jsonTweets)
    to_csv(tweets)


if __name__ == "__main__":
    main(
        keywords=['Google'],
        filename='twitterOutput.json',
        byUser=True,
        overwrite=True)
