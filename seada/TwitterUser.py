class TwitterUser():
    """Information about a Twitter user"""

    def __init__(self):
        self.id = ""
        self.id_str = ""
        self.name = ""
        self.screen_name = ""
        self.location = ""
        self.description = ""
        self.url = ""
        self.protected = ""
        self.followers_count = ""
        self.friends_count = ""
        self.listed_count = ""
        self.created_at = ""
        self.favourites_count = ""
        self.geo_enabled = ""
        self.verified = ""
        self.profile_image_url = ""
        self.profile_image_url_https = ""

    def set_user(self, user):
        # print("type of user: " + str(type(user)))
        # print("type of user.name: " + str(type(user.name)))
        # print("Type of user.entities: " + str(type(user.entities)))

        # print(user)
        # print(user.screen_name)
        # print(user.name)
        self.id = user.id
        self.id_str = user.id_str
        self.name = user.name
        self.screen_name = user.screen_name
        self.location = user.location
        self.description = user.description
        self.url = user.url
        self.protected = user.protected
        self.followers_count = user.followers_count
        self.friends_count = user.friends_count
        self.listed_count = user.listed_count
        self.created_at = user.created_at
        self.favourites_count = user.favourites_count
        self.geo_enabled = user.geo_enabled
        self.verified = user.verified
        self.profile_image_url = user.profile_image_url
        self.profile_image_url_https = user.profile_image_url_https
