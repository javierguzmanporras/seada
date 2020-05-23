# -*- coding: utf-8 -*-

from seadaIngest.outputInterface import OutputInterface
from seadaIngest.outputUtilities import OutputUtilities

import json


class TwitterFavorites(OutputInterface):
    """Information about a Twitter user's Favorites"""

    def __init__(self, user_id, favorite):
        self.user_id = user_id
        self.favorite = favorite

    def get_csv_output(self, file_name: str, dataset_directory: str):
        item = self.get_tuple_output()
        OutputUtilities.get_csv_output(file_name=file_name, dataset_directory=dataset_directory, item=item)

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
        text = self.favorite.text.replace("\n", "")

        # You could pickle/marshal/json your array and store it as binary/varchar/json field in your database.
        hashtags_json = json.dumps(self.favorite.entities_hashtags)
        user_mentions_json = json.dumps(self.favorite.entities_user_mentions)
        urls_json = json.dumps(self.favorite.entities_urls)

        tuple_favorites = (self.favorite.id, self.user_id, str(self.favorite.created_at), text,
                           self.favorite.source, str(self.favorite.place),
                           self.favorite.retweet_count, self.favorite.favorite_count, self.favorite.lang,
                           hashtags_json, user_mentions_json, urls_json)

        return tuple_favorites
