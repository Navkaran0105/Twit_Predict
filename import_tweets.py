import tweepy
import time
import json
import csv

consumer_key = "mpJ1S0PWPPcIx1XVn4aYPjWis"
consumer_secret = "cy8NO2TqPucdfhAttiQapa2GJOFnLamTaEegjzakH9C6lps42D"
access_key = "1000023816251281408-tribGTbICH7Oj0Vxe0WrWY2KIqXFBl"
access_secret = "qDLXrgE2DBjEnjAQMv8WMYQoEVivOTB84lEsmko3w0iR4"

conn = tweepy.OAuthHandler(consumer_key, consumer_secret)
conn.set_access_token(access_key, access_secret)
api = tweepy.API(conn)

csvFile = open('political_tweets_nbpoli.csv', 'w', newline='')
csvWriter = csv.writer(csvFile)

for tweet in tweepy.Cursor(api.search, 
                    q="#nbpoli",
                    lang="en").items(20000):
    if (not tweet.retweeted):
        csvWriter.writerow([tweet.text.encode('utf-8')])

csvFile.close()

