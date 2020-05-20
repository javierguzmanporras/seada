# -*- coding: utf-8 -*-

from outputInterface import OutputInterface
from outputUtilities import OutputUtilities


class TwitterFollowers(OutputInterface):
    """Information about a Twitter user's followers"""

    def __init__(self, user_id, follower_id):
        self.user_id = user_id
        self.follower_id = follower_id

    def get_csv_output(self, file_name: str, dataset_directory: str):
        pass

    def get_json_output(self, file_name: str, dataset_directory: str):
        """
                Call to outputUtilities class for generate a json file from user's friends information.
                If the file exists, append new item
                :return:
                """
        item = {'follower_id': self.follower_id, 'user_id': self.user_id}
        OutputUtilities.get_json_output(file_name=file_name, dataset_directory=dataset_directory,
                                        item=item, datatag='followers_list')

    def get_tuple_output(self) -> tuple:
        pass

