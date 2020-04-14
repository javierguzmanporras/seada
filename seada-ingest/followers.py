#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import tweepy
from tqdm import tqdm


class Followers:

    def __init__(self):
        self.user_followers = []

    def get_user_followers(self, api, username):

        nfollowers = 0

        user = api.get_user("@jgp_ingTeleco")
        my_total = user.followers_count

        for follower in tqdm(tweepy.Cursor(api.followers_ids, screen_name=username).items(), total=my_total,
                           desc="Get Followers"):
            try:
                follower_user = api.get_user(follower)
                self.user_followers.append(follower_user.screen_name)
                # print(str(nfriends) + " friend name: " + user.screen_name)
                nfollowers += 1
            except:
                print("error" + str(sys.exc_info()))

        print("[followers] Num of followers: " + str(nfollowers))
        print(self.user_followers)

