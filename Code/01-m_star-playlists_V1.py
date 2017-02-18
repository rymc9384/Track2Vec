# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 10:15:17 2017

@author: rbm166

Run Date: 02/17/2017, ~12:30pm EST
"""

import os
import time
import pickle
import re                                  # Version: 2.2.1
import spotipy                             # Version: 2.0.1
import spotipy.util as util

from utils.set_environment import SetVars  # Local code for setting environment vars


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


#################################################
### 1) GET FIRST 100,050 'm*' PLAYLISTS:
#################################################    

# Search for playlists with 'm*' in them:
lim_play = 50
search = sp.search(q='m*', limit=lim_play, type='playlist', market='US')

# Pull out the results and how many items were returned:
results = search['playlists']
total = len(results['items'])

# Decide how many playlists we're going to grab: (max is 100,050 - per Spotify)
n = search['playlists']['total']
if n > 1e+5 + 51:
    n = 1e+5


# Pull playlist IDs from 'results' and put into a list:
play_ids = [i['id'] for i in results['items']]

# Do the same for owner IDs -- (playlist owners):
owner_ids = [i['owner']['id'] for i in results['items']]

# keep track of errors:
errors = []


# Initialize the number of requests made:
count = 1

## While we haven't gotten the lesser of matched playlists or 100,050;
## keep repeating the search and grabbing the new results:
    
while total < n:
    
    time.sleep(5)   # minimize reliance on `spotipy` to handle HTTP status 429
    
    # try except for token timeouts:
    try:
        search = sp.next(results)   # Try the search straight up
        if search == None:
            raise TypeError("Search didn't yield results... 0 length.")
    except:
        token = util.prompt_for_user_token(username, scope)
        sp = spotipy.Spotify(auth=token)
        
        old_url = results['href']
        
        off_search = re.search('offset=[0-9]*(?=\&)',old_url)
        temp_offset = int(re.split('offset=',off_search.group(0))[1])
        temp_offset += lim_play
        
        temp_url = (old_url[:off_search.start()], \
                    str('offset=' + str(temp_offset)), \
                    old_url[off_search.end():])
        
        new_url = ''.join(temp_url)
        r = sp._session.request(method='GET', url=new_url)
        
        if r.status_code == 500 or r.status_code == 204:
            errors.append({'status':500, 'offset':temp_offset})
            search = sp.search(q='m*', limit=lim_play, type='playlist', \
                               market='US', offset=temp_offset+lim_play)
            total += lim_play
            
        elif r.status_code == 200:
            search = sp.next(results)
            
        else:
            print("There's an error, but I don't know what it is")
            break
            
    # subsetting results and updating our total:
    results = search['playlists']
    total += len(results['items'])
    
    # playlist and owner ids for current results:
    play_temp = [i['id'] for i in results['items']]
    owner_temp = [i['owner']['id'] for i in results['items']]
    
    # add those to our `master` list:
    play_ids += play_temp
    owner_ids += owner_temp
    
    # give some user feedback and update our count of requests made:
    if count % 5 == 0:
        print('Request', count, ':', total, '\n')
    
    count += 1
    
    
    
    
out = {'playlistid':play_ids,
       'ownerid':owner_ids }

with open('..\Data\m_star-playlists.txt', 'wb') as outfile:
    pickle.dump(out, outfile)