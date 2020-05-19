# -*- coding: utf-8 -*-

import sys
import logging
import tweepy
from tqdm import tqdm

from twitterTweet import Tweet


class TweetMiner:

    def __init__(self, api, username, num_tweets):
        self.api = api
        self.username = username
        self.num_tweets = num_tweets

        self.tweets_instances = []
        self.friends_id_list = []
        self.followers_id_list = []
        self.favorites_list = []

    def mine_tweets(self, api, screen_name, num_tweets):
        for tweet in tqdm(tweepy.Cursor(api.user_timeline,
                                        screen_name=screen_name,
                                        tweet_mode="extended").items(num_tweets),
                          desc="[+] Get Tweets",
                          total=num_tweets):
            t = Tweet()
            t.set_tweet_information(tweet)
            self.tweets_instances.append(t)

        return self.tweets_instances

    def mine_friends(self):
        user = self.api.get_user(self.username)
        total = user.friends_count
        print('[+] Retrieving {total} friends from {username}'.format(total=total, username=self.username))
        try:
            for friend_id in tqdm(tweepy.Cursor(self.api.friends_ids, screen_name=self.username).items(total),
                                  total=total, desc="[+] Get Friends"):
                self.friends_id_list.append(friend_id)
                # friend = self.api.get_user(friend_id)
                # self.friends_user_list.append(friend)
        except Exception as exception:
            print("[+] Error: {}. More info: {}".format(exception, sys.exc_info()))
            logging.critical('[TwitterFriends.get_user_friends] Error {}'.format(sys.exc_info()))

        return self.friends_id_list

    def mine_followers(self):
        user = self.api.get_user(self.username)
        total = user.followers_count
        print('[+] Retrieving {total} followers from {username}'.format(total=total, username=self.username))
        for follower_id in tqdm(tweepy.Cursor(self.api.followers_ids, screen_name=self.username).items(total),
                                total=total, desc="[+] Get Followers"):
            try:
                self.followers_id_list.append(follower_id)
                # api_follower_user = self.api.get_user(follower_id)
                # tu = TwitterUser("")
                # tu.set_user_information(api_follower_user)
                # self.followers_user_list.append(tu)
            except Exception as exception:
                print("[+] Error: {}. More info: {}".format(exception, sys.exc_info()))
                logging.critical("[TwitterFollowers.get_user_followers] Error {}".format(sys.exc_info()))

        return self.followers_id_list

    def mine_favorites(self):
        user = self.api.get_user(self.username)
        total = user.favourites_count
        print('[+] Retrieving {total} favorites from {username}'.format(total=total, username=self.username))
        try:
            for favorite in tqdm(tweepy.Cursor(self.api.favorites, screen_name=self.username).items(total),
                                 total=total, desc="[+] Get Favorite"):
                tweet = Tweet()
                tweet.set_tweet_information(favorite)
                self.favorites_list.append(tweet)
        except Exception as exception:
            print("[+] Error: {}. More info: {}".format(exception, sys.exc_info()))
            logging.critical("[TwitterFavorites.get_user_favorites] Error: {}".format(sys.exc_info()))

        return self.favorites_list
