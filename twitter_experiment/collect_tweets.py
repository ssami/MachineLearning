
# coding: utf-8

# In[5]:

import pandas as pd
import os, sys


# In[14]:

tweet_dir = 'tweets_raw'
full_tweets = os.getcwd() + os.sep + tweet_dir
files = os.listdir(full_tweets)


# In[66]:

# grab the first 99 tweets
df = pd.DataFrame()
df2 = pd.read_csv(full_tweets + os.sep + 'tweets_lang_99.csv', sep='\t', header=None)


# In[27]:

df.append(df2).head()


# Now we can clearly see that tweets are problematic in terms of languages. Not only do we need to deal with non-alphanumeric characters, we also have to remove part-alphanumerics, like mentions, hashtags and others. We can't remove specific character sets either. We can also look at the list of character ranges for emoticons here: http://apps.timwhitlock.info/emoji/tables/unicode. Most of them start with \xE or \xF so we could use that to clean up the strings more. So we'll start by implementing some filters. Below is a very hacky way of removing these basic things. 

# In[1]:

import re
mention_patt = r'(\@\w*)'
hash_patt = r'(\#\w*)'
url_patt = r'(http[s?]\:\/\/.*\s)'
emotic_patt = r'(^[\xe0-\xf0])'
test = "@Dinaa_ElAraby اها يا بيبي والله اتهرست علي تويتر و ع #keek some english https://t.co/vOR/aVpTnJ9?q=b  🌹🌹🌹🌹 text"
print "Before: ", test
replaced = re.sub(mention_patt, '', test)
print "After mention replacement:\t", replaced
replaced = re.sub(hash_patt, '', replaced)
print "After hashtag replacement:\t", replaced
replaced = re.sub(url_patt, '', replaced)
print "After url replacement:\t", replaced
#eplaced = re.sub(emotic_patt, '', replaced)
print "After emoticon replacement:\t", replaced


# Now we can read in every CSV file, clean every tweet and load everything in to CSV. 

# In[ ]:

import re 

def apply_patterns(string, patterns): 
    if string is None: 
        return string
    repl_str = string
    for p in patterns: 
        repl_str = re.sub(p, '', repl_str) 

    return repl_str


def clean_tweets(DataFrame df):     
    mention_patt = r'(\@\w*)'
    hash_patt = r'(\#\w*)'
    url_patt = r'(http[s?]\:\/\/.*\s)'
    emotic_patt = r'(^[\xe0-\xf0])'
    list_patt = [mention_patt, hash_patt, url_patt, emotic_patt]
    cleaned_df = DataFrame(data=None, columns=['tweet', 'lang']) 
    for index, row in df.iterrows():
        tweet = row[0] # the tweet itself 
        cltw = apply_patterns(tweet, list_patt)
        lang = row[1]     
        
        tmp = DataFrame(data=data, columns=['tweet', 'lang'], index=range(len(data))) 
        cleaned_df.append(tmp) 
        
        
        


