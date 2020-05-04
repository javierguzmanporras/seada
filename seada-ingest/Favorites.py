#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
from tqdm import tqdm
import tweepy


class Favorites:

    def __init__(self):
        self.user_followers = []


    def get_user_favorites(self, api, username):

        username = '@jgp_ingTeleco'

        user = api.get_user(username)

        user_favorites_count = user.favourites_count

        print('User {} has {} favorites'.format(username, user_favorites_count))

        for favorite in tqdm(tweepy.Cursor(api.favorites, screen_name=username).items(1),
                             total=1,
                             desc="Get Favorite"):
            try:
                print(favorite)
                time.sleep(2)
            except:
                print("error" + str(sys.exc_info()))