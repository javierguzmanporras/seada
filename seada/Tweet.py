#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Tweet():
    languages = {}
    sources = {}
    places = {}
    hashtags = {}

    def __init__(self):
        self.created_at = ""
        self.id = ""
        self.id_str = ""
        self.text = ""
        self.truncated = ""
        self.source = ""
        self.in_reply_to_status_id = ""
        self.in_reply_to_status_id_str = ""
        self.in_reply_to_user_id = ""
        self.in_reply_to_user_id_str = ""
        self.in_reply_to_screen_name = ""
        #user
        self.coordinates = ""
        self.place = ""
        self.contributors = ""
        self.is_quote_status = ""
        self.retweet_count = ""
        self.favorite_count = ""
        self.favorited = ""
        self.retweeted = ""
        self.possibly_sensitive = ""
        self.lang = ""
        #self.user_name = ""
        self.tuit = {}
        self.entities_hashtags = []
        self.entities_user_mentions = []
        self.entities_urls = []
    

    def set_tuit_information(self, item):
        self.created_at = item.created_at
        self.tuit['created_at'] = str(item.created_at)
        #self.id = item.id
        #self.tuit['id'] = item.id
        self.id_str = item.id_str
        self.tuit['id_str'] = item.id_str
        self.text = item.full_text
        self.tuit['text'] = item.full_text
        self.truncated = item.truncated
        self.tuit['truncated'] = item.truncated
        self.source = item.source
        self.tuit['source'] = item.source
        self.in_reply_to_status_id = item.in_reply_to_status_id
        self.tuit['in_reply_to_status_id'] = item.in_reply_to_status_id
        self.in_reply_to_status_id_str = item.in_reply_to_status_id_str
        self.tuit['in_reply_to_status_id_str'] = item.in_reply_to_status_id_str
        self.in_reply_to_user_id = item.in_reply_to_user_id
        self.tuit['in_reply_to_user_id'] = item.in_reply_to_user_id
        self.in_reply_to_user_id_str = item.in_reply_to_user_id_str
        self.tuit['in_reply_to_user_id_str'] = item.in_reply_to_user_id_str
        self.in_reply_to_screen_name = item.in_reply_to_screen_name
        self.tuit['in_reply_to_screen_name'] = item.in_reply_to_screen_name
        self.coordinates = item.coordinates
        self.tuit['coordinates'] = item.coordinates
        self.place = item.place
        self.tuit['place'] = item.place
        self.contributors = item.contributors
        self.tuit['contributors'] = item.contributors
        self.is_quote_status = item.is_quote_status
        self.tuit['is_quote_status'] = item.is_quote_status
        self.retweet_count = item.retweet_count
        self.tuit['retweet_count'] = item.retweet_count
        self.favorite_count = item.favorite_count
        self.tuit['favorite_count'] = item.favorite_count
        self.favorited = item.favorited
        self.tuit['favorited'] = item.favorited
        self.retweeted = item.retweeted
        self.tuit['retweet'] = item.retweeted
        #self.possibly_sensitive = item.possibly_sensitive
        #self.tuit['possibly_sensitive'] = item.possibly_sensitive
        self.lang = item.lang
        self.tuit['lang'] = item.lang

        e = item.entities
        if len(e['hashtags']) > 0:
            for hastag in e['hashtags']:
                self.entities_hashtags.append(hastag['text'])

        if len(e['user_mentions']) > 0:
            for mention in e['user_mentions']:
                self.entities_user_mentions.append(mention['screen_name'])

        if len(e['urls']) > 0:
            for url in e['urls']:
                self.entities_urls.append(url['expanded_url'])

        self.tuit['hashtags'] = self.entities_hashtags
        self.tuit['user_mentions'] = self.entities_user_mentions
        self.tuit['urls'] = self.entities_urls

        #if self.truncated:
        #    print(item.text_)

        #get lang
        if item.lang in self.languages:
            self.languages[item.lang] += 1
        else:
            self.languages[item.lang] = 1

        #get source
        if item.source in self.sources:
            self.sources[item.source] += 1
        else:
            self.sources[item.source] = 1

        #get places
        if item.place:
            if item.place.name in self.places:
                self.places[item.place.name] += 1
            else:
                self.places[item.place.name] = 1

        for ht in self.entities_hashtags:
            if ht in self.hashtags:
                self.hashtags[ht] += 1
            else:
                self.hashtags[ht] = 1

    @classmethod
    def get_report(self):
        for key, val in self.languages.items():
            print(str(key) + " => " + str(val))

        for key, val in self.sources.items():
            print(str(key) + " => " + str(val))

        for key, val in self.places.items():
            print(str(key) + " => " + str(val))

        for key, val in self.hashtags.items():
            print(str(key) + " => " + str(val))