# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 18:52:26 2017

@author: rbm166


NOTE: You HAVE TO delete the cache before doing this again or it 
      throws an error about scope.
      
      
TO_DO: 1) Add in looping functionality to gather playlists 
            1a) Can only offset by max of 100k so need to think about how to 
                constrain the search so that we get <= 100,050 results;
       2) Add in try excepts for refreshing token; 
       3) Add in waiting function if we make too many requests;
       4) ...

"""

import os
import time
import json                                # Version: 2.0.9
import spotipy                             # Version: 2.0.1
import spotipy.util as util
import pandas as pd                        # Version: 0.19.2

from utils.set_environment import SetVars  # Local code for setting environment vars

########################
### 0) AUTHORIZATION & INITIALIZATION:
    
# Coding jokes...
just = SetVars()
just.do_it()

username = os.getenv('SPOTIPY_USER_ID')
scope = 'user-library-read'

token = util.prompt_for_user_token(username, scope)

sp = spotipy.Spotify(auth=token)



########################
### 1) GETTING PLAYLISTS:
    
## Search for playlists from a genre so that we can pull tracks from those:    
a_list = sp.search('a*',limit=50,type='playlist',market='US') 

# Note that when going full scale, we'll want to loop over these b/c the total 
# should be greater than our limit (most of the time). We can do this with 
# the ``offset`` argument *OR* with the ``sp.next(a_list)`` command.

## Put the playlists into a dataframe:
playlists = pd.DataFrame(a_list['playlists']['items'])

# We are mostly interested in the playlist `id` column and the `owner`['id'].


########################
### 2) GETTING SONGS:
               
## Loop over playlists and retrieve the songs:                                                      
limit = 100

info = {}


for i in range(len(playlists)):
    
    user_temp = playlists.owner[i]['id']
    play_temp = playlists.id[i]
    
    info[play_temp] = {}
    
    returned = sp.user_playlist_tracks(user=user_temp,playlist_id=play_temp, \
                                       fields='total,items(track(name,id,artists(id)))', \
                                       limit=limit)
    time.sleep(1)
    
    # lists to hold track id, track name, and artist ids for playlist:
    t_id_play = []
    t_name_play = []
    a_id_play = []
    
    # put the requested items into a list
    temp_tracks = returned['items']
    
    # loop over the request while there are still unretrieved songs:
    count = limit

    while returned['total'] > count:
        time.sleep(2)
        returned = sp.user_playlist_tracks(user=user_temp,playlist_id=play_temp, \
                                       fields='total,items(track(name,id,artists(id)))', \
                                       limit=limit,offset=count)
        temp_tracks += returned['items']
        count += limit
    
    # loop over the tracks to put the pieces into their own lists:
    for t in temp_tracks:
        t_id_play.append(t['track']['id'])
        t_name_play.append(t['track']['name'])
        
        a_id_tr = []
        for a in t['track']['artists']:
            a_id_tr.append(a['id'])
        a_id_play.append(a_id_tr)
        
    info[play_temp]['trackid'] = t_id_play
    info[play_temp]['trackname'] = t_name_play
    info[play_temp]['artistid'] = a_id_play
        

    
## Write out data:
    
with open('data.txt', 'w') as outfile:
    json.dump(obj=info, fp=outfile, indent=0, separators=(',',':'))