# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 15:10:35 2017

@author: rbm166
"""

import pickle
import glob 


###################################
### FUNCTIONS:
###################################

##
## 1) Track ID to Artist Info Dictionary:
## 

def tID_aInfo(data,id_info=None):
    """
    This function takes one of the track info JSON files and generates a 
    dictionary that translates a track ID to the artist/album info associated 
    w/ that song; i.e., artist/album ID(s), artist/album name(s), and uri(s).
    
    NOTE: Same as tID_tInfo() function in "03-make_corpus-and-lookup_dict.py
    
    Args In: 
            1) 'data' = dict 
                - A dictionary with the structure defined by 
                    utils.playlist_funcs.splitter()
                    
            2) 'id_info' = dict
                - Existing dictionary w/ tracks from earlier playlists
    
    Returns:
            1) 'id_info' = dict
                - A dictionary mapping track IDs to human-readable info.
    """
    
    ## Initialize a dictionary to hold the track info:
    if id_info == None:    
        id_info = {}
    
    ## Loop over playlists and grab their track ids:
    for d in data:
                
        track_list = list(data[d].keys())
        
        for t in track_list:
            if t == None:
                continue
            
            existing = t in id_info.keys()
            
            if not existing:
                id_info[t] = data[d][t]
        
    return(id_info)



###############################################################################
###############################################################################
###############################################################################

    
###################################
### 0) CONFIGURATION
###################################

## Lookup Table end file:
artist_lookup_out = '../Data/TrackID_Artist_Lookup.txt'
album_lookup_out = '../Data/TrackID_Album_Lookup.txt'

## In-data files:
artist_files = glob.glob('../Data/PlaylistInfo/m_star-artists_info_*')
album_files = glob.glob('../Data/PlaylistInfo/m_star-albums_info_*')



###################################
### 1) ARTIST LOOKUP TABLE
###################################


#########
# 1a) Making dictionary

for i in range(len(artist_files)):
    
    print('Starting on file', i, ':', artist_files[i], '\n')
    
    with open(artist_files[i], 'rb') as f:
        data = pickle.load(f)
        
    if i == 0:
        id_info = None

    ## Lookup dictionary:
    id_info = tID_aInfo(data,id_info)
    
  
#########
# 1b) Writing out dictionary:
with open(artist_lookup_out, 'wb') as f:
    pickle.dump(id_info, f)
    
    
    
###################################
### 2) ALBUM LOOKUP TABLE
###################################

#########
# 2a) Making dictionary

for i in range(len(album_files)):
    
    print('Starting on file', i, ':', album_files[i], '\n')
    
    with open(album_files[i], 'rb') as f:
        data = pickle.load(f)
        
    if i == 0:
        id_info = None

    ## Lookup dictionary:
    id_info = tID_aInfo(data,id_info)
    
  
#########
# 2b) Writing out dictionary:
with open(album_lookup_out, 'wb') as f:
    pickle.dump(id_info, f)