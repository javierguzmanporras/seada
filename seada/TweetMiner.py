#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
from Tweet import *
from tqdm import tqdm


class TweetMiner:

    def __init__(self):
        self.tweets_instances = []
        self.tweets = []

    def mine_tweets(self, api, screen_name, num_tweets):
        for tweet in tqdm(tweepy.Cursor(api.user_timeline,
                                        screen_name=screen_name,
                                        tweet_mode="extended").items(num_tweets),
                          desc="Get Tweets",
                          total=num_tweets):
            t = Tweet()
            t.set_tweet_information(tweet)
            self.tweets.append(t.tweet)
            self.tweets_instances.append(t)

        return self.tweets_instances, self.tweets



