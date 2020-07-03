#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
from datetime import datetime

from elasticsearch import Elasticsearch


class ElasticSearchUtils:

    # seadaIngest's vars
    twitter_user_index_name = "twitter_user"
    twitter_user_mapping_file = "elasticsearch_twitter_user_index_mapping.json"
    twitter_tweet_index_name = "twitter_tweets"
    twitter_tweet_mapping_file = "elasticsearch_twitter_tweets_index_mapping.json"
    twitter_friend_index_name = "twitter_friends"
    twitter_friend_mapping_file = "elasticsearch_twitter_friends_index_mapping.json"
    twitter_follower_index_name = "twitter_follower"
    twitter_follower_mapping_file = "elasticsearch_twitter_follower_index_mapping.json"
    twitter_favorite_index_name = "twitter_favorite"
    twitter_favorite_mapping_file = "elasticsearch_twitter_favorite_index_mapping.json"

    # streaming's vars
    twitter_streaming_tweet_index_name = 'twitter_streaming_tweets'
    twitter_streaming_tweet_mapping_file = "elasticsearch_twitter_tweets_index_mapping.json"

    # seadaAlert's vars
    twitter_alert_index_name = 'twitter_alert'
    twitter_alert_mapping_file = 'elasticsearch_twitter_alert_index_mapping.json'

    def __init__(self, es_host, es_port):
        self.es_host = es_host
        self.es_port = es_port
        self.es_connection = ""

    def connect_elasticsearch(self):
        _es = None
        _es = Elasticsearch([{'host': self.es_host, 'port': self.es_port}])
        if _es.ping():
            print("[+] Connected to elasticsearch...")
            logging.info("[ElasticsearchUtils.connect] - Connected to elasticsearch...")
        else:
            print('[ElasticsearchUtils.connect] - Fail to connected to elasticsearch...')
            logging.critical("[ElasticsearchUtils.connect] - Fail to connected to elasticsearch...")
        return _es

    def create_index(self, index_name, mapping_file, debug, path='seadaIngest/elastic/'):
        try:
            if not self.es_connection.indices.exists(index_name):
                print('[+] Index {} not found.'.format(index_name))
                print('[+] Creating index in elasticsearch...')
                logging.warning("[elasticsearchUtils.create_index] Index " + index_name + " not found.")
                logging.info("[elasticsearchUtils.create_index] Creating index in elasticsearch...")

                path = path + mapping_file
                with open(path, 'r') as mf:
                    data = mf.read()

                index_definition = json.loads(data)
                response = self.es_connection.indices.create(index=index_name, body=index_definition)

                if debug:
                    print(str(response) + str('\n'))

                logging.info("[elasticsearchUtils.create_index]" + str(response))
        except Exception as e:
            print('[+] Exception: {}'.format(e))
            logging.critical('[elasticsearchUtils.create_index] Error in indexing data')

    def store_information_to_elasticsearch(self, index_name, info, debug):
        result = None
        document = dict(info)
        document['@timestamp'] = datetime.now()

        try:
            response = self.es_connection.index(index=index_name, id=document['id'], body=document)
            result = response['result']
            if debug:
                print('[+] {}'.format(response))

            logging.info("[elasticsearchUtils.ingest_user_information_to_elasticsearch]" + str(response))
        except Exception as es:
            print('[+] Exception at store info in database: {}'.format(es))
            logging.critical("[elasticsearchUtils.ingest_user_information_to_elasticsearch]" + str(es))

        return result
