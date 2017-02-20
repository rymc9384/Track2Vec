# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 14:41:13 2017

@author: rbm166
"""

class playlist_split():
    
    def splitter(self, response, fields=True, has_meta=True):
        """
        This function takes a response from the Spotify API asking for a user's 
        playlist info, and splits it up into smaller chunks that can be more 
        easily dealt with and written out to a database.
        
        Args In: 
                1) 'response' = (dict) the Spotify API response with all fields.
        
                2) 'fields' = ([strings] OR bool) what you want to get back 
                    - NOT IMPLEMENTED YET!!
                    - The default (TRUE) returns all fields; to get specific ones 
                        back use a list of strings
                    
                3) 'has_meta' = (bool) does 'response' have the meta-data?
        
        Returns:
                1) out = dictionaries w/ field specific data
        """
        
        # Can't feed it nothing:
        if response == None:
            print ('Input cannot be type None!')
            return(0)
        
        # Initialize dictionaries:
        tracks = {}
        artists = {}
        albums = {}
        
        # Decide what the returned `total` is:
        if has_meta:
            total = response['total']
        else:
            total = None
         
        # create temp
        response = response['items']
        
        # Getting the track info: 
        for t in response:
            if t!= None:
                if t['track'] != None:
                    t_id = t['track']['id']
                    tracks[t_id] = {'name':t['track']['name'],                  # String
                                    'popularity':t['track']['popularity'],      # Float
                                    'duration_ms':t['track']['duration_ms'],    # Long
                                    'explicit':t['track']['explicit'],          # Bool
                                    'uri':t['track']['uri']}                    # String
                        
                
                    artists[t_id] = {'ids':[x['id'] for x in t['track']['artists']],        # List of strings
                                     'names':[x['name'] for x in t['track']['artists']],    # List of strings
                                     'uris':[x['uri'] for x in t['track']['artists']]}      # List of strings
                    
                    albums[t_id] = {'id':t['track']['album']['id'],             # String
                                    'name':t['track']['album']['name'],         # String
                                    'type':t['track']['album']['type'],         # String
                                    'uri':t['track']['album']['uri']}           # String
                else:
                    pass
            else:
                pass
        # Put into list so that we can return that:
        if has_meta:
            out = [tracks,artists,albums,total]
        else:
            out = [tracks,artists,albums]
            
        # Return the `out` object:
        return(out)




    