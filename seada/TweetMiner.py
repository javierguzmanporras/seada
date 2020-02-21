#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from Tweet import *
import csv


class TweetMiner():

    def __init__(self):
        self.tweets = []

    def get_json_output(self):
        with open('tuit.json', mode='w', encoding='utf8') as tuit_file:
            json.dump(self.tweets, tuit_file, indent=4) #indent=4 nos formatea la salida del texto.

    def toString(self, jsonInformation):
        """convert json to string"""
        json_str = json.dumps(jsonInformation._json)
        #print(type(json_str))
        #print(json_str)

    def mine_tweet(self, api, username):
        timeline = api.user_timeline(screen_name=username, include_rts=True, count=500, page=1, tweet_mode="extended")
        print('#tweets: ' + str(len(timeline)))
        for item in timeline:
            #print(type(item))
            self.toString(item)
            t = Tweet()
            t.set_tuit_information(item)
            self.tweets.append(t.tuit)

    def get_report(self):
        Tweet.get_report()


