#!/usr/bin/python3
import json
import csv
from string import punctuation

def get_words(tweet):
        words = tweet.split(" ")
        return words

with open('test_data.csv') as csvfile:
        reader = csv.reader(csvfile)
        dict = open("Lexicon_dict.json")
        dict_obj = dict.read()
        data = json.loads(dict_obj)
        with open('labelled_test.csv','w',newline='') as analysis:
                writer = csv.writer(analysis)
                writer.writerow(['Tweet','Sentiment'])
                for row in reader:
                        score = 0
                        count = 0
                        tweet = row[0]
                        words = get_words(tweet)
                        print(words)
                        #for word in words:
                        for word in words:
                                if word in data:
                                        obj = data[word]
                                        score = score + obj['score']
                                        count = count + 1
                        if(count!=0):
                                score = score/count
                                if score < 0: 
                                        sentiment = 'negative'
                                else:
                                        sentiment = 'positive'
                                writer.writerow([tweet,sentiment])
