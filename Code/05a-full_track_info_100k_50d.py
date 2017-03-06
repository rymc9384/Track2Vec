# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 15:24:50 2017

@author: rbm166
"""

import pickle

###################################
### FUNCTIONS:
###################################

##
## 1) Decide to put track info into vocab data or not
## 

def into_vocab_data(vocab,lookup,lookupkeys,component):
    """
    This function takes one of the lookup tables that translate track id to 
    song, artist, or album info and puts the relevant items into a vocab data
    dictionary.
    
    Args In: 
            1) 'vocab' = dict 
                - A dictionary containing the information for a track that 
                  exists in the GloVe model vocabulary
                    
            2) 'lookup' = dict
                - Existing dictionary w/ track ID to info translation
                
            3) 'lookupkeys' = list
                - List containing the track IDs in the lookup table    
            
            4) 'component' = str
                - String telling function what the lookup dictionary is 
                  translating track IDs to.
                - Possible values \in ['track','artist','album']
    
    Returns:
            1) 'vocab' = dict
                - A dictionary with info for all the songs in a GloVe model's 
                  vocabulary.
    """
    
    ###################################
    ### Create Constants:
    # i) for component == 'track':
    vocab_track_keys = ['track_name','track_duration','track_explicit',\
                        'track_popularity','track_uri']
    comp_track_keys =['name','duration_ms','explicit','popularity','uri']
    
    # ii) for component == 'artist':
    vocab_artist_keys = ['artist_names','artist_ids','artist_uris']
    comp_artist_keys = ['names','ids','uris']
    
    # iii) for component == 'album':
    vocab_album_keys = ['album_name','album_id','album_type','album_uri']
    comp_album_keys = ['name','id','type','uri']
    ###################################
    
    
    # Make sure we have a valid input:
    if component not in ['track','artist','album']:
        raise ValueError

    # Make list of vocab keys:
    vkeys = list(vocab.keys())

    # Initialize count variable:
    count = 0    
    n = len(vkeys)
    
    # begin if looking at tracks:
    if component == 'track':
        # begin for loop over the vocab keys, pulling info from matching keys:
        for k in vkeys:
            
            # begin for loop over the keys containing track info:
            for i in range(len(vocab_track_keys)):
                vocab[k][vocab_track_keys[i]] = lookup[k][comp_track_keys[i]]
            # end for i; keys w/ track info         
            # begin if count is divisible by 1000:
            if count % 1000 == 0:
                print(count,"/", n, "\n")
            
            count +=1
            # end if count is divisible by 1000
        # end for k; keys marking track ids
        
    # end if component == 'track'
    # begin if we're looking at artist info:
    elif component == 'artist':
        # begin for loop over the vocab keys, pulling info from matching keys:
        for k in vkeys:
            # begin for loop over the keys containing track info:
            for i in range(len(vocab_artist_keys)):
                vocab[k][vocab_artist_keys[i]] = lookup[k][comp_artist_keys[i]]
            # end for i; keys w/ track info
            # begin if count is divisible by 1000:
            if count % 1000 == 0:
                print(count,"/", n, "\n")
            
            count +=1
            # end if count is divisible by 1000
        # end for k; keys marking track ids
        
    # end if component == 'artist'
    # begin if we're looking at album info:      
    elif component == 'album':
        # begin for loop over the vocab keys, pulling info from matching keys:
        for k in vkeys:
            # begin for loop over the keys containing track info:
            for i in range(len(vocab_album_keys)):
                vocab[k][vocab_album_keys[i]] = lookup[k][comp_album_keys[i]]
            # end for i; keys w/ track info
            # begin if count is divisible by 1000:
            if count % 1000 == 0:
                print(count,"/", n, "\n")
            
            count +=1
            # end if count is divisible by 1000
        # end for k; keys marking track ids
    # end if component == 'album'
    
    return(vocab)


###################################
### 0) CONFIGURATION
###################################

#########
# 0a) Reading in the 'vocabulary' (i.e., track IDs):
vocab_file = 'E:/Users/rbm166/Desktop/GloVe_Spotify/vocab100k_50d.txt'
with open(vocab_file, 'r') as f:
    vocablist = f.readlines()

# Remove the 'ROOT', 'END' and 'DUMMY' items:
for i in range(3):
    vocablist.pop(0)

#########
# 0b) Putting vocabulary into dictionary, with one item being the frequency:
vocab = {}
for v in vocablist:
    temp_v = v.split(' ')
    vocab[temp_v[0]] = {}
    vocab[temp_v[0]]['freq'] = int(temp_v[1].strip('\n'))

###################################
### 1) ADDING TRACK INFO TO VOCAB
###################################

## Load track lookup table (explicit, duration_ms, name, uri, popularity):
with open('..\Data\TrackID_Lookup.txt', 'rb') as f:
    tab = pickle.load(f)

keys = list(tab.keys())


## Apply function:
vocab = into_vocab_data(vocab=vocab,lookup=tab,lookupkeys=keys,component='track')
del tab


###################################
### 2) ADDING ARTIST INFO TO VOCAB
###################################

## Load artist lookup table (ids, names, uris):
with open('..\Data\TrackID_Artist_Lookup.txt', 'rb') as f:
    tab = pickle.load(f)

keys = list(tab.keys())


## Apply function:
vocab = into_vocab_data(vocab=vocab,lookup=tab,lookupkeys=keys,component='artist')
del tab



###################################
### 3) ADDING ALBUM INFO TO VOCAB
###################################

## Load album lookup table (id, name, type, uri):
with open('..\Data\TrackID_Album_Lookup.txt', 'rb') as f:
    tab = pickle.load(f)

keys = list(tab.keys())


## Apply function:
vocab = into_vocab_data(vocab=vocab,lookup=tab,lookupkeys=keys,component='album')
del tab


###################################
### 4) WRITE OUT VOCAB TO PICKLE
###################################

with open('E:/Users/rbm166/Desktop/GloVe_Spotify/Lookup_Vocab100k_50d.txt', 'wb') as f:
    pickle.dump(vocab, f)