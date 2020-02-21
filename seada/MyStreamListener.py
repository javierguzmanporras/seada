import tweepy


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        #print(status.text)
        print(status)

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_error disconnects the stream
            return False

        # returning non-False reconnects the stream, with backoff.