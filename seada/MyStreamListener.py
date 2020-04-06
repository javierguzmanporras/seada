import tweepy

from TwitterUser import *
from Tweet import *


class MyStreamListener(tweepy.StreamListener):

    def __init__(self, args, db, connection, dataset_directory):
        super(MyStreamListener, self).__init__()
        self.args = args
        self.db = db
        self.connection = connection
        self.dataset_directory = dataset_directory
        self.ntweets = 0

    def on_status(self, status):
        """"
        To retrieve, process and organize tweets to get structured data and inject data into database or elasticsearch.
        :param status:
        :return:
        """
        t = Tweet()
        t.set_tweet_information(status)
        self.db.create_tweet(self.connection, t.get_tuple_output_without_raw())
        self.ntweets = self.ntweets + 1
        print("[MyStreamListener] Add new tweet: " + str(self.ntweets))

        return True

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_error disconnects the stream
            return False

        # returning non-False reconnects the stream, with backoff.