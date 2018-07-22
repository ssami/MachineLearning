#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
url_patt = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'\".,<>?«»“”‘’]))"
# giant url pattern from http://daringfireball.net/2010/07/improved_regex_for_matching_urls
emotic_patt = r'(^[\xe0-\xf0])'
test = "@Dinaa_ElAraby اها يا بيبي والله اتهرست علي تويتر و ع #keek some english https://t.co/vOR/aVpTnJ9?q=b  🌹🌹🌹🌹 text"
print "Before: ", test
replaced = re.sub(mention_patt, '', test)
print "After mention replacement:\t", replaced
replaced = re.sub(hash_patt, '', replaced)
print "After hashtag replacement:\t", replaced
replaced = re.sub(url_patt, '', replaced)
print "After url replacement:\t", replaced
replaced = re.sub(emotic_patt, '', replaced)
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


#TODO: NEED to start index range from last index of incoming DF
def clean_tweets(df, ind):     
    mention_patt = r'(\@\w*)'
    hash_patt = r'(\#\w*)'
    url_patt = r'(http[s?]\:\/\/.*\s)'
    emotic_patt = r'(^[\xe0-\xf0])'
    list_patt = [mention_patt, hash_patt, url_patt, emotic_patt]
    data = []
    for index, row in df.iterrows():
        tweet = row[0] # the tweet itself 
        cltw = apply_patterns(tweet, list_patt)
        lang = row[1]
        tup = (cltw, lang) 
        data.append(tup) 

    tmp = pd.DataFrame(data=data, columns=['tweet', 'lang'], index=range(ind, ind+len(data))) 
    return tmp   
        
def load_small_csv(loc): 
    files = os.listdir(loc)
    print "Loading csv files from ", loc
    file_count = 0
    cleaned_df = pd.DataFrame(data=None, columns=['tweet', 'lang']) 
    for c in files: 
        f = loc + os.sep + c
        try: 
            df = pd.read_csv(f, sep='\t', header=None) 
            count = df.count(axis=0)[0]
            file_count += count
            cleaned_df = cleaned_df.append(clean_tweets(df, count))
            #print "So far: ", cleaned_df.count(axis=0)['tweet'] 
        except Exception as e: 
            print "Could not load " + f + " because " + str(e) 
        
    
    print "Total count: ", cleaned_df.count(axis=0)['tweet'] 
    print "Sanity check: ", file_count
    return cleaned_df  


all_loaded = load_small_csv('tweets_raw')
all_loaded.to_csv('tweets_collected.tsv', sep='\t', columns=['tweet', 'lang'])
