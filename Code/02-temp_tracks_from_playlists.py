# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 17:12:55 2017
Last Edited on Mon Feb 20 14:29:38 2017

@author: rbm166

"""

import os
#import time
import pickle
#
#import re                                       # Version: 2.2.1
import spotipy                                  # Version: 2.0.1
import spotipy.util as util

from utils.set_environment import SetVars       # Local code for setting environment vars
from utils.playlist_funcs import playlist_split # Local code for dealing w/ API responses

#################################################
### 0) AUTHORIZATION & INITIALIZATION:
#################################################   

# Coding jokes...
just = SetVars()
just.do_it()

username = os.getenv('SPOTIPY_USER_ID')
scope = 'user-library-read'

token = util.prompt_for_user_token(username, scope)
sp = spotipy.Spotify(auth=token)


#dummy_url = 'https://api.spotify.com/v1/tracks/3n3Ppam7vgaVa1iaRUc9Lp'
#r = sp._session.request('GET',dummy_url)

#################################################
### 1) READ IN PLAYLIST DATA:
################################################# 

with open('..\Data\m_star-playlists.txt', 'rb') as infile:
    data = pickle.load(infile)
    
    
#################################################
### 2) GET PLAYLIST SPECIFIC DATA:
################################################# 

# initialize the function to deal with API responses:
pFun = playlist_split()


# initialize dictionaries:
track_info = {}
artist_info = {}
album_info = {}

# request limit
lim_track = 100

# number of playlists in our dataset:
playlist_n = len(data['playlistid'])

# out file info:
n_files_out =                      # updated for restart.

#for i in range(playlist_n):
#for i in range(3000,playlist_n):    # restart at 3,000; no such user error at 3,032
for i in range(17807,playlist_n):    # restart at 17,807; no 'total' key at 17,806
    
    user_temp = data['ownerid'][i]
    play_temp = data['playlistid'][i]
    
    try:
        response = sp.user_playlist_tracks(user=user_temp,playlist_id=play_temp, \
                                       limit=lim_track)
    except spotipy.SpotifyException as e:
        err_str = e.msg.split(':\n ')[-1]
        if err_str == 'No such user':
            print('Playlist', i, ':', err_str, '- skipping. \n')
            continue
        elif err_str == 'The access token expired':
            token = util.prompt_for_user_token(username, scope)
            sp = spotipy.Spotify(auth=token)
            response = sp.user_playlist_tracks(user=user_temp,playlist_id=play_temp, \
                                       limit=lim_track)
        else: 
            print('Playlist', i, ':', err_str)
            whatdo = None
            while whatdo not in ['continue', 'break']:
                whatdo = input("Please enter 'continue' *OR* 'break'. \n")
            
            if whatdo == 'continue':
                continue
            else:
                break
    
    #time.sleep(1)
    
    x = pFun.splitter(response=response, fields=True, has_meta=True)
    
    ## Add track info:
    track_info[play_temp] = x[0]
    
    ## Add artist info:
    artist_info[play_temp] = x[1]
    
    ## Add album info:
    album_info[play_temp] = x[2]
    
    
    # loop over the request while there are still unretrieved songs:
    total = x[3]
    count = lim_track
    
    while total > count:
        #time.sleep(2)
        try:
            response = sp.user_playlist_tracks(user=user_temp, \
                                               playlist_id=play_temp, \
                                               fields='items', \
                                               limit=lim_track,offset=count)
        except spotipy.SpotifyException as e:
            err_str = e.msg.split(':\n ')[-1]
            if err_str == 'The access token expired':
                token = util.prompt_for_user_token(username, scope)
                sp = spotipy.Spotify(auth=token)
                response = sp.user_playlist_tracks(user=user_temp, \
                                               playlist_id=play_temp, \
                                               fields='items', \
                                               limit=lim_track,offset=count)
                
            else:
                print('Playlist', i, ':', err_str)
                whatdo = None
                while whatdo not in ['continue', 'break']:
                    whatdo = input("Please enter 'continue' *OR* 'break'. \n")
                
                if whatdo == 'continue':
                    continue
                else:
                    break
                
        x = pFun.splitter(response=response, fields=True, has_meta=False)
        
        # update dictionaries:
        track_info[play_temp].update(x[0])
        artist_info[play_temp].update(x[1])
        album_info[play_temp].update(x[2])
        
        count += lim_track
        
    
    # User feedback:
    print('Playlist ', str(i), ': ', str(total), ' tracks. \n')
             
    # Intermediate write out of data, and reset dicts :
    if i >0 and i % 500 == 0 or i >= playlist_n:
        fout = '..\Data\PlaylistInfo\m_star-tracks_info_' + str(n_files_out) + '.txt'
        with open(fout, 'wb') as f:
            pickle.dump(track_info, f)
            
        track_info = {}
        
        fout = '..\Data\PlaylistInfo\m_star-artists_info_' + str(n_files_out) + '.txt'
        with open(fout, 'wb') as f:
            pickle.dump(artist_info, f)
            
        artist_info = {}
        
        fout = '..\Data\PlaylistInfo\m_star-albums_info_' + str(n_files_out) + '.txt'
        with open(fout, 'wb') as f:
            pickle.dump(album_info, f)
            
        album_info = {}
        
        n_files_out += 1
        
        
        
 
