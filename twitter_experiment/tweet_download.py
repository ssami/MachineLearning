# coding: utf-8
#!/usr/bin/env python

# In[1]:

import requests, base64, json, urllib, time, re
import pandas as pd
import sys

twidx = sys.argv[1]

# In[2]:

#gets bearer access token
oauth_url = 'https://api.twitter.com/oauth2/token'
consumer_key = open('_cons_key').readlines()[0].strip()
consumer_secret = open('_cons_secret').readlines()[0].strip()

# In[3]:

uenc_con_key = consumer_key # right now encoding doesn't change format
uenc_con_secret = consumer_secret # right now encoding doesn't change format
concat_string = uenc_con_key + ':' + uenc_con_secret
b64_concat_string = base64.b64encode(concat_string)

# In[4]:

body = "grant_type=client_credentials"
headers = {}
headers['Authorization'] = 'Basic ' + b64_concat_string
headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'
print(headers)


# In[5]:

r = requests.post(oauth_url, data=body, headers=headers)


# In[6]:

r.status_code


# In[7]:

r.text


# In[8]:

cleaned_data = '/Users/ssami/Git_personal/MachineLearning/twitter_experiment/notebooks/twitter_cleaned_uniformly_sampled.tsv'
tdata = pd.DataFrame.from_csv(cleaned_data, sep='\t')
sample_count = tdata['tweet_id'].count()

# In[9]:

access_token = r.json()['access_token']
#print access_token
b64_bearer = base64.b64encode(access_token)
headers = {}
headers['Authorization'] = 'Bearer ' + access_token
#print headers


# In[ ]:

tweet_csv_prefix = 'tweets_lang_'
csv_suffix = '.csv'


# In[ ]:

tweet_url = 'https://api.twitter.com/1.1/statuses/lookup.json?id='
tweet_number = 99
idx = int(twidx)  
delim = ','
sleep_time = 10

print "Starting index: ", idx
print "Sample count: ", sample_count

while idx < sample_count: 
    print "Current index: ", idx
    # batch call to get 99 tweets
    tweet_full = tweet_url + str(tweet_number) + delim
    idx_end = idx + tweet_number
    ids = ""
    
    # concat tweet ids 
    for i in tdata.iloc[idx:idx_end]['tweet_id']: 
        ids += str(i) + delim
        
    tweet_full = tweet_full + ids[:-1] # remove last comma 
    tweet_full = tweet_full[:-1]
    
    # make requests for 99 tweets at a time
    r = requests.get(tweet_full, headers=headers)
    
    # if the status is not successful, 
    # continue without changing idx
    # so we can re-try the index 
    if (r.status_code != 200):
        print "error: " + r.text
        time.sleep(60)
        continue
    tweet = r.text
    jtweet = json.loads(tweet)
    lang_list = []
    text_list = []
    # store found tweets and corresponding langs
    for t in jtweet: 
        if t['text'] is not None and len(t['text']) > 0: 
            text = t['text']
            text = re.sub('\n', '', text)
            lang_loc = tdata[tdata['tweet_id'] == t['id']]
            if not lang_loc.empty:
                lang = lang_loc['language'].values[0]
                lang_list.append(lang)
                text_list.append(text)
        else: 
            print t['id'] + " not found!"
    
    # write to data structure
    smp = []
    smp = zip(text_list, lang_list)
    
    # store in temporary csv file 
    idx += tweet_number
    csv_name = tweet_csv_prefix + str(idx) + csv_suffix
    df = pd.DataFrame(data=smp, columns=['tweet', 'lang'])
    df.to_csv(csv_name, index=False, header=False, sep='\t', encoding='utf-8')
    time.sleep(sleep_time)

