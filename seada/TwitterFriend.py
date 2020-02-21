#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import sys
from tqdm import tqdm

class Friends():
    """Information about a Twitter user's friends"""

    def __init__(self):
        #self.user_id = ""
        self.user_friends = []

    def get_user_friends(self,api,username):

        nfriends = 0

        user = api.get_user("@jgp_ingTeleco")
        my_total = user.friends_count

        for userid in tqdm(tweepy.Cursor(api.friends_ids, screen_name=username).items(), total=my_total,
                           desc="Get Friends"):
            try:
                user = api.get_user(userid)
                self.user_friends.append(user)
                #print(str(nfriends) + " friend name: " + user.screen_name)
                nfriends += 1
            except:
                print("error" + str(sys.exc_info()))


        print("Num friends: " + str(nfriends))
        if "arduino" in self.user_friends:
            print("arduino ok")

        if "algoquenoesta" in self.user_friends:
            print("algoquenoesta ko")

            #https://www.rittmanmead.com/blog/2015/08/three-easy-ways-to-stream-twitter-data-into-elasticsearch/