# -*- coding: utf-8 -*-

from seadaIngest.outputUtilities import OutputUtilities
from seadaIngest.outputInterface import OutputInterface


class TwitterFriend(OutputInterface):
    """Information about a Twitter user's friends"""

    def __init__(self, user_id, friend_id):
        self.user_id = user_id          # User's friend ID
        self.friend_id = friend_id      # Friend ID

    def get_csv_output(self, file_name: str, dataset_directory: str):
        """"""
        item = self.get_tuple_output()
        OutputUtilities.get_csv_output(file_name=file_name, dataset_directory=dataset_directory, item=item)

    def get_json_output(self, file_name: str, dataset_directory: str):
        """
        Generate a json file from user's friends information. If the file exists, append new item
        :return: a new json file, or a new item
        """
        item = {'friend_id': self.friend_id, 'user_id': self.user_id}
        OutputUtilities.get_json_output(file_name=file_name, dataset_directory=dataset_directory,
                                        item=item, datatag='friend_list')

    def get_tuple_output(self) -> tuple:
        tuple_friend = (self.friend_id, self.user_id)
        return tuple_friend
