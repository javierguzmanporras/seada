# -*- coding: utf-8 -*-

import sys
import logging
import tweepy
from tqdm import tqdm

from seadaIngest.twitterTweet import Tweet
from seadaIngest.twitterFriend import TwitterFriend
from seadaIngest.twitterFollower import TwitterFollowers
from seadaIngest.twitterFavorites import TwitterFavorites


class TweetMiner:

    def __init__(self, api, username, num_tweets):
        self.api = api
        self.username = username
        self.num_tweets = num_tweets

    def mine_tweets(self):
        tweets_instances = []
        for tweet in tqdm(tweepy.Cursor(self.api.user_timeline,
                                        screen_name=self.username,
                                        tweet_mode="extended").items(self.num_tweets),
                          desc="[+] Get Tweets",
                          total=self.num_tweets):
            t = Tweet()
            t.set_tweet_information(tweet)
            tweets_instances.append(t)

        return tweets_instances

    def mine_friends(self):
        friends_instances = []
        friends_id_list = []
        user = self.api.get_user(self.username)
        total = user.friends_count
        print('[+] Retrieving {total} friends from {username}'.format(total=total, username=self.username))
        try:
            for friend_id in tqdm(tweepy.Cursor(self.api.friends_ids, screen_name=self.username).items(total),
                                  total=total, desc="[+] Get Friends"):
                friend = TwitterFriend(user_id=self.username, friend_id=friend_id)
                friends_instances.append(friend)
                friends_id_list.append(friend_id)
        except Exception as exception:
            print("[+] Error: {}. More info: {}".format(exception, sys.exc_info()))
            logging.critical('[TwitterFriends.get_user_friends] Error {}'.format(sys.exc_info()))

        return friends_instances, friends_id_list

    def mine_followers(self):
        followers_instance = []
        followers_id_list = []
        user = self.api.get_user(self.username)
        total = user.followers_count
        print('[+] Retrieving {total} followers from {username}'.format(total=total, username=self.username))
        for follower_id in tqdm(tweepy.Cursor(self.api.followers_ids, screen_name=self.username).items(total),
                                total=total, desc="[+] Get Followers"):
            try:
                follower = TwitterFollowers(user_id=self.username, follower_id=follower_id)
                followers_instance.append(follower)
                followers_id_list.append(follower_id)
            except Exception as exception:
                print("[+] Error: {}. More info: {}".format(exception, sys.exc_info()))
                logging.critical("[TwitterFollowers.get_user_followers] Error {}".format(sys.exc_info()))

        return followers_instance, followers_id_list

    def mine_favorites(self):
        favorites_instance = []
        user = self.api.get_user(self.username)
        total = user.favourites_count
        print('[+] Retrieving {total} favorites from {username}'.format(total=total, username=self.username))
        try:
            for favorite in tqdm(tweepy.Cursor(self.api.favorites, screen_name=self.username).items(total),
                                 total=total, desc="[+] Get Favorite"):
                tweet = Tweet()
                tweet.set_tweet_information(favorite)
                favorite = TwitterFavorites(self.username, tweet)
                favorites_instance.append(favorite)
        except Exception as exception:
            print("[+] Error: {}. More info: {}".format(exception, sys.exc_info()))
            logging.critical("[TwitterFavorites.get_user_favorites] Error: {}".format(sys.exc_info()))

        return favorites_instance
