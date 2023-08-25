import tweepy as tw
import pandas as pd

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

#----------------------------------------------

search_words = "Donald Trump"
date_since = "2013-03-01"

tweets = tw.Cursor(api.search,
                   q=search_words,
                   lang="en",
                   since=date_since).items()

#-------------------------------------------------

for tweet in tweets:
    print(tweet.text)
#-------------------------------------------------

import tweepy

date_since = "2013-03-01"

auth = tweepy.OAuthHandler('dC0Yca95LoJfpaZbqnXvpOIxghT1bBX',
                           'YNi3GfHgzVWls7si7MXdrhAhshhgQIfqfKiTVdXrf7mPPfCaY6RdhBFd2VADa')
auth.set_access_token = (
'8085s0353-YCsrdoLzcxyjrtpch9Y5djoduUcqhKzqNbBdayJvdvEg0O', 'jIqd2Gdr17uicnIc4c7c3czpXfErj82BGjksXQdD5a7WMVc7Sumj')
api = tweepy.API(auth)
tweets = tweepy.Cursor(api.search, q="nousinfosystem", tweet_mode='extended', since=date_since).items(3500)

#--------------------------------------------------

from tqdm import tqdm

tweets_dict_list = []

for t in tqdm(tweets):
    d = {}
    d['created_at'] = t.created_at
    d['favorite_count'] = t.favorite_count
    d['retweet_count'] = t.retweet_count
    d['full_text'] = t.full_text
    d['screen_name'] = t.user.screen_name

    tweets_dict_list.append(d)

#--------------------------------------------------

for tweet in tqdm(tweets):
    print(tweet.full_text)

#---------------------------------------------------









