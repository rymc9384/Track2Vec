# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 12:02:02 2017

@author: rbm166
"""

import pickle
import glob 


###################################
### FUNCTIONS:
###################################

##
## 1) Corpus Writing Function:
## 
  
def corpus_writing(data,corp_out,root=True,end=True,dummywords=True, \
                   dummy_len=5,append=True):
    """
    This function takes one of the track info JSON files and writes out the 
    track id to an outfile -- effectively making our corpus for a GloVe model.
    
    Args In: 
            1) 'data' = dict 
                - A dictionary with the structure defined by 
                    utils.playlist_funcs.splitter()
                  
            2) 'corp_out' = string 
                - The file that we're writing our corpus to
                
            3) 'root' = bool 
                - Add 'ROOT' to the start of a playlist's tracks
    
            4) 'end' = bool 
                - Add 'END' to the end of a playlist's tracks
    
            5) 'dummywords' = bool 
                - Separate the tracks of different playlists with some dummy 
                    'words' (i.e., fake tracks)
                    
            6) 'dummy_len' = int
                - If adding dummy words, how many to put between playlists.   
    
            7) 'append' = bool 
                -Are we writing a new file or adding onto an existing one?
    
    Returns:
            1) A text file with the track ids white-spaced delimited
    """
    
    ## Initialize a list to hold the track IDs:
    temp_corp = []
    
    ## Loop over playlists and grab their track ids:
    for d in data:
        
        ## If we want 'ROOT' to start a playlist:
        if root:
            temp_corp.append('ROOT ')
        
        ## Add in the track IDs:
        track_list = list(data[d].keys())
        try:
            temp_corp.append(' '.join(track_list))
        except TypeError: # essentially if there's a None type element
            track_list.pop(track_list.index(None))
        
        ## Adding 'END' and/or dummy words:
        if end and dummywords:
            temp_corp.append(' END ')
            for i in range(dummy_len):
                temp_corp.append('DUMMY ')
        #        
        elif end and not dummywords:
            temp_corp.append(' END ')
        #   
        elif dummywords and not end:
            temp_corp.append(' DUMMY ')
            
            for i in range(dummy_len - 1):
                temp_corp.append('DUMMY ')
        #        
        else:
            temp_corp.append(' ')
            
    
    temp_corp = ''.join(temp_corp)
    
    if append:
        with open(corp_out, 'a') as f:
            f.write(temp_corp)
    else:
        with open(corp_out, 'w') as f:
            f.write(temp_corp)
    
######################################################
######################################################
    
##
## 2) Track ID to Track Info Dictionary:
## 
    
def tID_tInfo(data,id_info=None):
    """
    This function takes one of the track info JSON files and generates a 
    dictionary that translates a track ID to the info associated w/ that song; 
    i.e., the name, length, etc...
    
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

## Writing Corpus Args:
root, end, dummywords = True, True, True
dummy_len = 5
corp_out = '../Data/corpus.txt'

## Lookup Table end file:
lookup_out = '../Data/TrackID_Lookup.txt'

## In-data files:
files = glob.glob('../Data/PlaylistInfo/m_star-tracks_info_*')


###################################
### 1) CREATING CORPUS AND LOOKUP TABLE
###################################


for i in range(len(files)):
    
    print('Starting on file', i, ':', files[i], '\n')
    
    with open(files[i], 'rb') as f:
        data = pickle.load(f)
        
    if i == 0:
        append = False
        id_info = None
    else: 
        append = True

    ## Corpus writing:
    corpus_writing(data,corp_out,root,end,dummywords,dummy_len,append)
    
    ## Lookup dictionary:
    id_info = tID_tInfo(data,id_info)
    
    
###################################
### 2) WRITE OUT LOOKUP TABLE
###################################

with open(lookup_out, 'wb') as f:
    pickle.dump(id_info, f)