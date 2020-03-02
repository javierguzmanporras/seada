#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import csv
import tweepy
import Utils
from Tweet import *
from Database import *


class TweetMiner:

    def __init__(self):
        self.tweets_instances = []
        self.tweets = []

    def get_json_output(self, file_name, dataset_directory):
        print('[TweetMiner][get_json_otput] #tweets: ' + str(len(self.tweets)))
        Utils.get_json_output(file_name, dataset_directory, self.tweets)

    def mine_tweets(self, api, screen_name, num_tweets):
        for tweet in tweepy.Cursor(api.user_timeline, screen_name=screen_name, tweet_mode="extended").items(num_tweets):
            t = Tweet()
            t.set_tweet_information(tweet)
            self.tweets.append(t.tweet)
            self.tweets_instances.append(t)

    def get_report(self):
        Tweet.get_report()

    def add_tweets_to_database(self, db, connection):
        for tweet in self.tweets_instances:
            db.create_tweet(connection, tweet.get_tuple_output())



