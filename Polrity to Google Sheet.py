#pip install textblob
#pip install indicoio
#pip install gspread
#oauth2client

#---------------------------------------------------------

import tweepy
from tqdm import tqdm
import numpy as np
import json
import pandas as pd
#import indicoio
import seaborn as sns
import json
import datetime as dt
from matplotlib import pyplot as plt
#% matplotlib inline

#---------------------------------------------------------

import tweepy as tw
from tqdm import tqdm

tweets_dict_list = []

auth = tw.OAuthHandler('XXX', 'YYY')
auth.set_access_token = ('ZZZ', 'AAA')
api = tw.API(auth)
# username = 'elonmusk'
# tweets = tweepy.Cursor(api.user_timeline,screen_name=username, tweet_mode='extended').items()

search_words = "RahulGandhi"
# '#AEM'
# "Adobe Experience Manager"
date_since = "2019-05-01"
date_until = "2019-05-31"
# ,             since=date_since

tweets = tw.Cursor(api.search,
                   q=search_words,
                   lang="en", since_date=date_since, until_date=date_until).items()

for t in tqdm(tweets):
    # print(t.text)
    # print(t.created_at)
    d = {}
    d['created_at'] = t.created_at
    d['favorite_count'] = t.favorite_count
    d['retweet_count'] = t.retweet_count
    d['text'] = t.text
    tweets_dict_list.append(d)

#--------------------------------------------------------------------

full_tweets = []
for item in tweets_dict_list:
    full_tweets.append(item['text'].lower().replace('\n', ' '))
    item['virality'] = item['favorite_count'] + item['retweet_count']

#---------------------------------------------------------------------

cleaned_tweets = []
for tweet in full_tweets:
    storage = []
    for word in tweet.split():
        if (len(word) < 3):
            continue
        if ('@' in word):
            continue
        if ('https://' in word):
            continue
        storage.append(word)
    cleaned_tweets.append(' '.join(storage))

for i, tweet in enumerate(tweets_dict_list):
    tweet['cleaned_text'] = cleaned_tweets[i]

#----------------------------------------------------------------------

import pandas as pd

df_tweets = pd.DataFrame.from_dict(tweets_dict_list)

#---------------------------------------------------------------------

from textblob import TextBlob
import re


def clean_tweet(tweet):
    '''
    Utility function to clean the text in tweet by removing links and special characters using regex
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


def analize_tweet(tweet):
    '''
    Utility function for classifying polarity of a tweet using Textblob
    '''
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        # return 1
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        # return 0
        return 'Neutral'
    else:
        # return -1
        return 'Negative'


#-------------------------------------------------------------------------

import numpy as np

df_tweets['SA'] = np.array([analize_tweet(tweet) for tweet in df_tweets['text']])

# pos_tweets = df_tweets[df_tweets['SA']>0]['text']
pos_tweets = df_tweets[df_tweets['SA'] == 'Positive']['text']
# neu_tweets = df_tweets[df_tweets['SA']==0]['text']
neu_tweets = df_tweets[df_tweets['SA'] == 'Neutral']['text']
# neg_tweets = df_tweets[df_tweets['SA']<0]['text']
neg_tweets = df_tweets[df_tweets['SA'] == 'Negative']['text']

#-------------------------------------------------------------------------

#import gspread as gc
#from oauth2client.service_account import ServiceAccountCredentials

#-------------------------------------------------------------------------

import os
from json import dumps

# SCOPES = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive"]

# creds = ServiceAccountCredentials.from_json_keyfile_name(os.path.join('D:/Ashwin/ds', 'SAFromPython-9ff59f90c392.json'), SCOPES)
# client = gspread.authorize(creds)

# sheet = client.open("Polarity").sheet1
# client.open("Polarity").get_worksheet(2)
# client.open("Polarity").sheet2

# list_of_hashes = sheet.get_all_records()
# print(list_of_hashes)
# sheet.update_cell(2, 1, "I just wrote to a spreadsheet using Python!")
# sheet.update_cell(3, 1, "Percepntage Positive Tweets: {}%".format(len(pos_tweets)*100/len(df_tweets['text'])) )
# sheet.update_cell(1, 1, "Percepntage Positive Tweets: {}%")
# sheet.update_cell(1, 2, (len(pos_tweets)*100/len(df_tweets['text'])) )
# sheet.update_cell(2, 1, "Percepntage Neutral  Tweets: ")
# sheet.update_cell(2, 2, (len(neu_tweets)*100/len(df_tweets['text'])) )
# sheet.update_cell(3, 1, "Percepntage Negetive Tweets: ")
# sheet.update_cell(3, 2,(len(neg_tweets)*100/len(df_tweets['text'])) )

print("Total Tweets:", len(df_tweets))
print("Total Positive Tweets:{}", len(pos_tweets))
print("Percepntage Positive Tweets: {}%".format(len(pos_tweets) * 100 / len(df_tweets['text'])))
print("Total Negetive Tweets:{}", len(neg_tweets))
print("Percecntage of Negative Tweets: ", (len(neg_tweets) * 100 / len(df_tweets['text'])))
print("Total Neutral Tweets:{}", len(neu_tweets))
print("Percecntage of Neutral Tweets: ", (len(neu_tweets) * 100 / len(df_tweets['text'])))

# print('A')

# rc = 6
# print('B')

# tqdm(tweets)

# for row in df_tweets.iterrows():
# print(t.text)
# print(t.created_at)
# tweetdate = dumps(row[1]['created_at'], default=default)
#   t = row[1]['created_at']
#   t = t.strftime('%m/%d/%Y')
#   ts = json.dumps(t)
#   sheet.update_cell(rc, 1,ts )
#   sheet.update_cell(rc, 2,row[1]['text'] )
#   sheet.update_cell(rc, 3,row[1]['favorite_count'] )
#   sheet.update_cell(rc, 4,row[1]['retweet_count'] )
#   sheet.update_cell(rc, 5,row[1]['SA'] )
#   rc = rc + 1

#-------------------------------------------------------------------------

#pip install cStringIO

#---------------------------------------------------------------

for row in df_tweets.iterrows():
    t = row[1]['created_at']
    t = t.strftime('%m/%d/%Y')
    txt = row[1]['text']
    fc = str(row[1]['favorite_count'])
    rc = str(row[1]['retweet_count'])
    sent = str(row[1]['SA'])
    print(' '.join([txt, '|', t, '|', fc, '|', rc, '|', sent]))

#------------------------------------------------------------------------

for pt in pos_tweets:
    print(pt)

#--------------------------------------------------------------------
