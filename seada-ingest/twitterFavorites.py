#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import tweepy
import logging

from tqdm import tqdm
from twitterTweet import Tweet


class TwitterFavorites:
    """Information about a Twitter user's Favorites"""

    def __init__(self, username, api):
        self.username = username
        self.api = api
        self.favorites_list = []

    def get_user_favorites(self):

        user = self.api.get_user(self.username)
        total = user.favourites_count

        print('[+] User {} has {} favorites'.format(self.username, total))

        try:
            for favorite in tqdm(tweepy.Cursor(self.api.favorites, screen_name=self.username).items(total),
                                 total=total, desc="[+] Get Favorite"):

                tweet = Tweet()
                tweet.set_tweet_information(favorite)
                self.favorites_list.append(tweet)
        except:
            print("[+] Error" + str(sys.exc_info()))
            logging.critical("[TwitterFavorites.get_user_favorites] Error: {}".format(sys.exc_info()))

    def get_output(self):
        for favorite in self.favorites_list:
            print(favorite.text)
