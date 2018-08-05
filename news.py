
from newsapi import NewsApiClient
import requests
import json
import csv

newsapi = NewsApiClient(api_key='82b9643a5c0449749d97a7ad96428cda')

response = newsapi.get_everything(q='New Brunswick liberals',sources='cbc',language='en')

print (response)

# wih open ('headlineslib.csv','a') as headlines 
#     writer = csv.writer(headlines)

# data = json.dumps(response)
# for item in data['source']:
#     writer.writerow(item.get('title'))

