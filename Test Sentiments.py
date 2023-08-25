import tweepy
from tqdm import tqdm
import numpy as np
import json
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
% matplotlib inline

#-----------------------------------------------------

This is the
program
after
troubleshooting
tweets
extract

import tweepy
from tqdm import tqdm

tweets_dict_list = []

auth = tweepy.OAuthHandler('XXX', 'YYY')
auth.set_access_token = ('ZZZ', 'AAA')
api = tweepy.API(auth)
username = 'elonmusk'
tweets = tweepy.Cursor(api.user_timeline, screen_name=username, tweet_mode='extended').items()

for t in tqdm(tweets):
    print(t.full_text)
    d = {}
    d['created_at'] = t.created_at
    d['favorite_count'] = t.favorite_count
    d['retweet_count'] = t.retweet_count
    d['full_text'] = t.full_text
    d['screen_name'] = t.user.screen_name

    tweets_dict_list.append(d)

#--------------------------------------------------------------

#Lets create column that measures how viral the tweet is!

full_tweets = []
for item in tweets_dict_list:
    full_tweets.append(item['full_text'].lower().replace('\n', ' '))
    item['virality'] = item['favorite_count'] + item['retweet_count']

#---------------------------------------------------------------

#Remove some special characters and https: // from the tweets

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

#---------------------------------------------------------------

# Basic exploration of tweets

import pandas as pd

df_tweets = pd.DataFrame.from_dict(tweets_dict_list)

------------------------------------------------------------

#Let us find descriptive statistics of numerical values in data

df_tweets.describe()

-----------------------------------------------------------

#Data Visualization

import numpy as np
import json
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
% matplotlib inline

fig, ax = plt.subplots(1, 2)
df_tweets.created_at.dt.weekday_name.value_counts().plot(kind='bar', figsize=(15, 5), ax=fig.axes[0])
ax[0].set_title('Maximum Usage days')
ax[0].set_ylabel('Number of tweets')
ax[0].set_xlabel('Date')

df_tweets.created_at.dt.hour.value_counts().nlargest(10).plot(kind='bar', figsize=(15, 5), ax=fig.axes[1])
plt.title("Maximum usage hours in a day")
plt.title('Number of tweets')
plt.xlabel('Date')

pip
install
plotly as py

import plotly.plotly as py
import plotly.graph_objs as go

df_tweet['Time'] = pd.to_datetime(df_tweets['created_at'], format='%y-%m-%d %H:%M:%S')
tweetsT = df_tweets['Time']
trace = go.Histogram(x=tweetsT, marker=dict(color='blue'), opacity=0.75)
layout = go.Layout(title='Tweets activity over the years', height=450, width=1200, xaxis=dict(title='Month and Year'),
                   yaxis=dict(title='Tweet Quantity'), bargap=0.2, )
data = [trace]
fig = go.Figure(data=data, layout=layout)
py.iplot(fig)

#------------------------------------------------------------

# Get most popular tweets

df_tweets_pop = df_tweets.groupby(['created_at', 'full_text'], as_index=False)['retweet_count'].sum().sort_values(
    by='retweet_count')
df_tweets_pop.tail(10)

---------------------------------------------------------------

# Lets analyze commonly used words in the tweets

pip install wordcloud

from wordcloud import WordCloud


def plot_wordcloud(msg):
    plt.figure(figsize=(8, 8))
    wordcloud = WordCloud(max_font_size=120, max_words=100, background_color="white").generate(", ".join(msg))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    img_path = "./wordcloud.png"
    wordcloud.to_file(img_path)


plot_wordcloud(df_tweets['cleaned_text'])

#-----------------------------------------------------------------

# Lets analyse sentiments

pip install textblob

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
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1


import numpy as np

df_tweets['SA'] = np.array([analize_tweet(tweet) for tweet in df_tweets['full_text']])
display(df_tweets.head(200))

pos_tweets = df_tweets[df_tweets['SA'] > 0]['full_text']
neu_tweets = df_tweets[df_tweets['SA'] == 0]['full_text']
neg_tweets = df_tweets[df_tweets['SA'] < 0]['full_text']

print("Percepntage Positive Tweets: {}%".format(len(pos_tweets) * 100 / len(df_tweets['full_text'])))
print("Percepntage Neutral  Tweets: {}%".format(len(neu_tweets) * 100 / len(df_tweets['full_text'])))
print("Percepntage Negetive Tweets: {}%".format(len(neg_tweets) * 100 / len(df_tweets['full_text'])))

import seaborn as sns
from matplotlib import pyplot as plt
% matplotlib inline

plt.figure(figsize=(10, 5))
# ns.barplot(data=df_tweets,x="Day_Name",y="retweet_count",hue="SA")
sns.barplot(data=df_tweets, x=df_tweets.created_at.dt.weekday_name, y="retweet_count", hue="SA")

plt.xticks(rotation=90)
plt.show()

------------------------------------------------------------------------------------

#Lets identify the Emotions

pip install indicoio from indicoio import political, sentiment, language, text_tags, keywords, fer

x_emotion = df_tweets.cleaned_text.values.tolist()

import indicoio

indicoio.config.api_key = 'af8ec2c2011ad98cb4a3856af355431e'

b = indicoio.emotion(x_emotion)
myvalues = [max(b[i], key=b[i].get) for i in range(len(b))]
df_tweets['emotion'] = pd.Series((v for v in myvalues))

b = indicoio.personality(x_emotion)
myvalues = [max(b[i], key=b[i].get) for i in range(len(b))]
df_tweets['personality'] = pd.Series((v for v in myvalues))

df_tweets.head()

df_tweets.emotion.value_counts().nlargest(10).plot(kind='barh', figsize=(10, 5))
plt.title("Emotions of tweets")
plt.ylabel("Number of tweets")
plt.xlabel("Date")

df_tweets.personality.value_counts().nlargest(10).plot(kind='barh', figsize=(10, 5))
plt.title("Personlaity Traits")
plt.ylabel("Number of tweets")
plt.xlabel("Date")
