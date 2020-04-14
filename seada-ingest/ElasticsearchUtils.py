#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
from datetime import datetime

from elasticsearch import Elasticsearch


class ElasticSearchUtils:

    def __init__(self, es_host, es_port):
        self.es_host = es_host
        self.es_port = es_port
        self.es_connection = ""

    def connect_elasticsearch(self):
        _es = None
        _es = Elasticsearch([{'host': self.es_host, 'port': self.es_port}])
        if _es.ping():
            print("[ElasticsearchUtils.connect] - Connected to elasticsearch...")
            logging.info("[ElasticsearchUtils.connect] - Connected to elasticsearch...")
        else:
            print('[ElasticsearchUtils.connect] - Fail to connected to elasticsearch...')
            logging.critical("[ElasticsearchUtils.connect] - Fail to connected to elasticsearch...")
        return _es

    def create_index(self, index_name, mapping_file):
        try:
            if not self.es_connection.indices.exists(index_name):
                print("[TwitterUser.create_index] Index " + index_name + "not found.")
                print("[TwitterUser.create_index] Creating index in elasticsearch...")

                path = "elastic/" + mapping_file
                with open('elastic/elasticsearch_twitter_user_index_mapping.json', 'r') as mapping_file:
                    data = mapping_file.read()

                index_definition = json.loads(data)

                print("[TwitterUser.create_index] " + str(type(index_definition)))
                print("[TwitterUser.create_index]" + str(index_definition))
                print()

                response = self.es_connection.indices.create(index=index_name, body=index_definition)
                print(response)
                print()
        except Exception as e:
            print('Error in indexing data')


    def store_information_to_elasticsearch(self, index_name, info):
        #index_name = "twitter_user"
        #doc_type = "user"
        #self.user['@timestamp'] = datetime.now()
        info['@timestamp'] = datetime.now()

        # print("id: " + str(type(self.user['id'])))
        # print("name: " + str(type(self.user['name'])))
        # print("screen_name: " + str(type(self.user['screen_name'])))
        # print("followers_count: " + str(type(self.user['followers_count'])))
        # print("friend_count: " + str(type(self.user['friends_count'])))
        # print("geo_enabled" + str(type(self.user['geo_enabled'])))

        #self.create_index(index_name=index_name)

        try:
            #response = self.elasticsearch.index(index=index_name, id=9, body=self.user)
            response = self.es_connection.index(index=index_name, id=info['id'], body=info)
            print("[TwitterUser.ingest_user_information_to_elasticsearch_v2]" + str(response))
        except Exception as es:
            print("[TwitterUser.ingest_user_information_to_elasticsearch_v2]" + str(es))