import tweepy
import socket
import requests
import time
import csv
import stat
import os
import socket
import json
import re

class TwitterStreamListener(tweepy.StreamListener):
 
        def __init__(self, sc):
                super(TwitterStreamListener, self).__init__()
                self.client_socket = sc
#                self.num_tweets = 0

        def on_status(self, status):
                tweet = self.get_tweet(status)
                self.client_socket.send((tweet[2]+"\n").encode())
 #               self.num_tweets +=1
 #              if self.num_tweets <= 50:
  #              	return True
   #             else:
    #            	return False

        def on_error(self, status_code):
                print("Status code")
                print(status_code)
                if status_code == 403:
                        print("The request is understood, but the access is not allowed. Limit may be reached.")
                        return False

        def get_tweet(self,tweet):
                text = tweet.text
                if hasattr(tweet, 'extended_tweet'):
                        text = tweet.extended_tweet['full_text']
                return [str(tweet.user.id),tweet.user.screen_name,self.clean_str(text)]

        def clean_str(self, string):
                """
                Tokenization/string cleaning.
                """
                # string = re.sub(ur'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', "", string, re.I | re.U)
                string = re.sub(r"\n|\t", " ", string)
                #string = re.sub(r"(.)\1{2,}", r"\1\1", string)
                #string = re.sub(r"(..)\1{2,}", r"\1\1", string)
                #string = re.sub(r"(...)\1{2,}", r"\1\1", string)
                #string = re.sub(r"(....)\1{2,}", r"\1\1", string)
                return string

if __name__ == '__main__':
        # Authentication
        consumer_key = "mpJ1S0PWPPcIx1XVn4aYPjWis"
        consumer_secret = "cy8NO2TqPucdfhAttiQapa2GJOFnLamTaEegjzakH9C6lps42D"
        access_token = "1000023816251281408-tribGTbICH7Oj0Vxe0WrWY2KIqXFBl"
        access_token_secret = "qDLXrgE2DBjEnjAQMv8WMYQoEVivOTB84lEsmko3w0iR4"

        # Local connection
        host = "127.0.0.1" # Get local machine name (copy internal address from EC2 instance).
        port = 5555                 # Reserve a port for your service.

        s = socket.socket()         # Create a socket object.
        s.bind((host, port))        # Bind to the port.

        print("Listening on port: %s" % str(port))

        s.listen(5)                 # Now wait for client connection.
        c, addr = s.accept()        # Establish connection with client.

        print("Received request from: " + str(addr))
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.secure = True
        auth.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=10, retry_delay=5, retry_errors=5)

        streamListener = TwitterStreamListener(c)
        myStream = tweepy.Stream(auth=api.auth, listener=streamListener, tweet_mode='extended')
        myStream.filter(track=['Canada','Nova Scotia','New Brunswick','Blaine Higgs'], async=True)
