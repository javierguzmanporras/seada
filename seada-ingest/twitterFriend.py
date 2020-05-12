#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import tweepy
import logging

from timer import Timer
from tqdm import tqdm


class TwitterFriends:
    """Information about a Twitter user's friends"""

    def __init__(self, username, api):
        self.api = api
        self.username = username
        self.friends_id_list = []        # List with user id of user's friends
        self.friends_user_list = []      # List with instances of twitterUser class

    def get_user_friends(self):
        user = self.api.get_user(self.username)
        total = user.friends_count

        for friend_id in tqdm(tweepy.Cursor(self.api.friends_ids, screen_name=user).items(total), total=total,
                            desc="Get Friends"):
            try:
                self.friends_id_list.append(friend_id)
                friend = self.api.get_user(friend_id)
                self.friends_user_list.append(friend)
            except:
                print("[+] Error " + str(sys.exc_info()))
                logging.critial('[TwitterFriends.get_user_friends] Error {}'.format(sys.exc_info()))

    def get_output(self):
        for friend in self.friends_user_list:
            print(friend.name)




