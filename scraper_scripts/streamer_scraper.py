#!/usr/bin/env python
# coding: utf-8

# In[40]:


import requests
import json
import pandas as pd
import time
import pprint
pp = pprint.PrettyPrinter(indent=4)

import psycopg2 as pg
from sqlalchemy import create_engine


# In[2]:


# Twitch Client ID 
clientID = 'vb2kmh60pt0tee6o2c11ko6n2t1w9a'

def get_top_100_games(clientID = clientID):
    ''' Given Client ID, pings twitch API for top 100 games. Returns the entire request object'''
    # Need to pass client ID with each request in header
    headers = {'Client-ID': clientID}
    url = '''https://api.twitch.tv/helix/games/top?first=100'''
    r = requests.get(url, headers=headers)
    return r

# r_dict = json.loads(r.text)


# In[3]:


def check_api_limit_reached(req, ignore_limit = False):
    '''Check remaining API pings for request REQ. If API requests is <=1, wait for 30s 
    so for all requests to refill. Returns remaining requests'''
    if int(req.headers['Ratelimit-Remaining']) <= 1: # No more requests, need to pause for 30s
        if ignore_limit:
            return int(req.headers['Ratelimit-Remaining'])
        print('Waiting for API limit to refresh (30s)...')
        time.sleep(30)
        print('Continuing...')
    return int(req.headers['Ratelimit-Remaining'])


# In[4]:


def get_top_100_streamers_for_each_game(game_dict):
    '''Given the twitch response for top 100 games, this will cycle through and pull the top 100
    streamers for each game, stored under a dict entry of the title of that game'''
    stream_dict = dict()
    headers = {'Client-ID': clientID}
    url = 'https://api.twitch.tv/helix/streams?first=100&game_id='
    for game in game_dict['data']:
        req = requests.get(url + game['id'],headers=headers)
        check_api_limit_reached(req)    
        stream_dict[game['name']]=json.loads(req.text)
    return stream_dict


# In[10]:


def json_to_dataframe(json_data):
    total_streams_df = pd.DataFrame(
        columns = ['game_id','id','language','started_at','title','type','user_id','user_name','viewer_count'])
    for game_key in list(json_data.keys()):
        game_streams_df = pd.io.json.json_normalize(json_data[game_key]['data'])
        total_streams_df = pd.concat([total_streams_df, game_streams_df], sort = False)
    total_streams_df.drop(columns = ['community_ids','thumbnail_url','tag_ids'], inplace = True)
    return total_streams_df


# In[15]:


def get_game_tags(clientID):
    # API call to for game tags
    return game_tags_json


# In[42]:


def run_all():
    r = get_top_100_games()
    r_dict = json.loads(r.text)

    stream_dict = get_top_100_streamers_for_each_game(r_dict)
    df=json_to_dataframe(stream_dict)

    df.rename(columns = {'id': 'stream_id','type': 'stream_type'},inplace = True)

    # Use this as the time stamp 
    curr_time = time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime())
    df['time_logged'] = curr_time
    passkey_path = "./rds_passkey.txt"
    passkey =  open(passkey_path, "r").read()
    # connection = pg.connect(host="twitchdata.chd4n5ul8muk.us-east-2.rds.amazonaws.com",
    #                               database="twitchdata",
    #                               user="postgres",
    #                               password=passkey, 
    #                               port=5432)
    
    engine = create_engine('postgresql://postgres:FwwBFmleh65qYxKxDVb9@twitchdata.chd4n5ul8muk.us-east-2.rds.amazonaws.com:5432/twitchdata')
    df.to_sql('stream_data', engine, if_exists='append',index=False)
    engine.dispose()

# In[ ]:


if __name__ == '__main__':
    run_all()

