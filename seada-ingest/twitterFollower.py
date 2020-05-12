#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import tweepy
import logging

from tqdm import tqdm
from twitterUser import TwitterUser


class TwitterFollowers:
    """Information about a Twitter user's followers"""

    def __init__(self, username, api):
        self.username = username
        self.api = api
        self.followers_id_list = []         # List with id of user's followers
        self.followers_user_list = []       # List with instances of twitterUser class

    def get_user_followers(self):

        user = self.api.get_user(self.username)
        total = user.followers_count

        for follower_id in tqdm(tweepy.Cursor(self.api.followers_ids, screen_name=user).items(total), total=total,
                             desc="Get Followers"):
            try:
                self.followers_id_list.append(follower_id)
                api_follower_user = self.api.get_user(follower_id)
                tu = TwitterUser("")
                tu.set_user_information(api_follower_user)
                self.followers_user_list.append(tu)
            except:
                print("[+] Error" + str(sys.exc_info()))
                logging.critical("[TwitterFollowers.get_user_followers] Error {}".format(sys.exc_info()))

    def get_output(self):
        for follower in self.followers_user_list:
            print(follower.name)

