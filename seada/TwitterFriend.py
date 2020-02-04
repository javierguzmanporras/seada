import tweepy


class Friends():
    """Information about a Twitter user's friends"""

    def __init__(self):
        pass

    def get_user_friends(self,api,username):

        nfriends = 0

        for userid in tweepy.Cursor(api.friends_ids, screen_name=username).items():
            user = api.get_user(userid)
            print(user.screen_name)
            nfriends += 1

        print("Num friends: " + str(nfriends))





    # code for print all friends
    # friends = api.friends_ids()
    # friends = api.friends(count=50)
    # print(len(friends))
    # for id in friends:
    #    print(id)