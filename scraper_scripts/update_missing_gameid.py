#!/usr/bin/env python
# coding: utf-8

# In[7]:


import requests
import json
import pandas as pd
from sqlalchemy import create_engine
import pprint
pp = pprint.PrettyPrinter(indent=4)
import psycopg2 as pg
import pandas.io.sql as pd_sql


# # Notebook used to detect games existing in streams data table that are not in the game_information table.

# Twitch Client ID 
clientID = 'vb2kmh60pt0tee6o2c11ko6n2t1w9a'


# In[ ]:


# Postgres info to connect (Only for manual queries)

# connection_args = {
#  "host": "twitchdata.chd4n5ul8muk.us-east-2.rds.amazonaws.com",
#  "user": "postgres",
#    "password":"FwwBFmleh65qYxKxDVb9",
#  "port": 5432,
#  "dbname": "twitchdata"
# }



def get_game_ids(clientID = clientID):
    ''' Grabs top 100 games from strem_data table that are not in game_information table,
    then grabs top 100 ID's. Returns request object from Twitch API '''
    
    # Set up Postgres info to connect and get query for game_ids in regularly updated database that are missing 

    connection_args = {
     "host": "twitchdata.chd4n5ul8muk.us-east-2.rds.amazonaws.com",
     "user": "postgres",
       "password":"FwwBFmleh65qYxKxDVb9",
     "port": 5432,
     "dbname": "twitchdata"
    }

    connection = pg.connect(**connection_args)

    query = '''SELECT DISTINCT(game_id) FROM stream_data
        WHERE game_id NOT IN (SELECT DISTINCT(game_id) FROM game_information) '''
    
    first_100_games = pd_sql.read_sql(query, connection).head(100)['game_id']

    headers = {'Client-ID': clientID}
    url = '''https://api.twitch.tv/helix/games'''
    for counter,game in enumerate(first_100_games):
        # First element requires ? before id=, the rest require &id=
        if counter == 0:
            url += '?id=' + game
        else:
            url += '&id=' + game
    r = requests.get(url, headers=headers)
    return r
def push_gameids_to_SQL(r):
    ''' Converts request object r to dataframe, then uses sqlalchemy create_engine object to push to
    SQL. Returns nothing'''
    game_df = pd.io.json.json_normalize(json.loads(r.text)['data'])

    game_df.rename(columns = {'id': 'game_id','name': 'game_name','box_art_url': 'pic_url'},inplace = True)
    print(game_df.head())
    engine = create_engine('postgresql://postgres:FwwBFmleh65qYxKxDVb9@twitchdata.chd4n5ul8muk.us-east-2.rds.amazonaws.com:5432/twitchdata')
    game_df.to_sql('game_information', engine, if_exists='append',index=False)
    engine.dispose()


def push_100_game_ids_to_sql():
    up_to_100_missing_game_ids = get_game_ids()
    push_gameids_to_SQL(up_to_100_missing_game_ids)

# Syntax for command line execution

if __name__ == '__main__':
    push_100_game_ids_to_sql()

