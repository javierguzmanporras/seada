# -*- coding: utf-8 -*-

from outputInterface import OutputInterface
from outputUtilities import OutputUtilities


class TwitterFavorites(OutputInterface):
    """Information about a Twitter user's Favorites"""

    def __init__(self, user_id, favorite):
        self.user_id = user_id
        self.favorite = favorite

    def get_csv_output(self, file_name: str, dataset_directory: str):
        pass

    def get_json_output(self, file_name: str, dataset_directory: str):
        """
        Generate a json file from user's friends information. If the file exists, append new item
        :return:
        """
        item = {
            'user_id': self.user_id,
            'favorite_created_at': str(self.favorite.created_at),
            'favorite_id': self.favorite.id,
            'favorite_text': self.favorite.text,
            'favorite_source': self.favorite.source,
            'favorite_coordinates': self.favorite.coordinates,
            'favorite_place': str(self.favorite.place),
            'favorite_retweet_count': self.favorite.retweet_count,
            'favorite_favorite_count': self.favorite.favorite_count,
            'favorite_lang': self.favorite.lang,
            'favorite_hashtags': self.favorite.entities_hashtags,
            'favorite_user_mentions': self.favorite.entities_user_mentions,
            'favorite_urls': self.favorite.entities_urls
        }

        OutputUtilities.get_json_output(file_name=file_name, dataset_directory=dataset_directory,
                                        item=item, datatag='favorites_list')

    def get_tuple_output(self) -> tuple:
        pass
