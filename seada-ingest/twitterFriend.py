#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import tweepy
import logging
import outputUtilities
from outputInterface import OutputInterface

from timer import Timer
from tqdm import tqdm


class TwitterFriends(OutputInterface):
    """Information about a Twitter user's friends"""

    def __init__(self, api):
        self.api = api
        self.friends_id_list = []        # List with user id of user's friends
        self.friends_user_list = []      # List with instances of twitterUser class

    def get_user_friends(self, username):
        user = self.api.get_user(username)
        total = user.friends_count
        try:
            for friend_id in tqdm(tweepy.Cursor(self.api.friends_ids, screen_name=username).items(total), total=total,
                                  desc="[+] Get Friends"):
                self.friends_id_list.append(friend_id)
                friend = self.api.get_user(friend_id)
                self.friends_user_list.append(friend)
        except Exception as exception:
            print("[+] Error: {}. More info: {}".format(exception, sys.exc_info()))
            logging.critical('[TwitterFriends.get_user_friends] Error {}'.format(sys.exc_info()))

    def get_output(self):
        for friend in self.friends_user_list:
            print(friend.name)

    def get_csv_output(self, file_name: str, dataset_directory: str):
       pass

    def get_json_output(self, file_name: str, dataset_directory: str):
        """
        Generate a json file from user's friends information. If the file exists, append new item
        :return: a new json file, or a new item
        """
        item = {'data': self.friends_id_list}
        outputUtilities.OutputUtilities.get_json_output(file_name=file_name, dataset_directory=dataset_directory, item=item)

    def get_tuple_output(self) -> tuple:
        pass



    #
    # def get_cvs_output(self, file_name, dataset_directory):
    #     """
    #     Generate a CVS file from user information instance. If the file exists, append info in new row.
    #     :return: a new csv file or a new row.
    #     """
    #     pass
    #
    # def get_tuple_output(self):
    #     pass





