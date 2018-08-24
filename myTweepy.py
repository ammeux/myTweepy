import tweepy
from TwitterCredentials import consumer_key, consumer_secret, access_token, access_token_secret
import time


# # # # TWITTER AUTHENTIFICATION # # # #
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


# # # # LIB INITIALIZATION # # # #
api = tweepy.API(auth)
cursor = tweepy.Cursor


# # # # HOME TIMELINE # # # #
class twitterCursor():

    def get_home_timeline(self):
        #get rate limit for home_timeline (15 request per 15 min window)
        data = api.rate_limit_status()
        print("Rate Limit for home_timeline:")
        print(data['resources']['statuses']['/statuses/home_timeline'])

        return tweepy.Cursor(api.home_timeline).items(10)

    def get_user_timeline(self, id, count):
        return api.user_timeline(screen_name = id, count = count)

# # # # TWITTER POST NEW TWEET # # # #
class twitterPoster():

    def post_new_tweet(self, message):
         api.update_status(message)

# # # # TWITTER STREAMER # # # #
class twitterStreamer(tweepy.StreamListener):

    def __init__(self, socketio):
        super().__init__()
        self.socketio = socketio

    def on_status(self, status):
        self.socketio.emit('my response', {'message':status._json})
        time.sleep(2)

    def on_error(self, status):
        print(status)

class newStream():

    def __init__(self, socketio):
        self.socketio = socketio

    def get_stream(self):
        myStreamListener = twitterStreamer(self.socketio)
        myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
        return(myStream)

# # # # GET USER DETAILS # # # #
class twitterUser():

    def get_user(self, id):
        myUser = api.get_user(id)
        return myUser
