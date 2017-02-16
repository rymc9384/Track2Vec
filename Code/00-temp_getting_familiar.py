# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 18:52:26 2017

@author: rbm166
"""

import os
import spotipy                       # Version: 2.0.1
import spotipy.util as util

from set_environment import SetVars  # Local code for setting environment vars

########################
### 0) AUTHORIZATION & INITIALIZATION:
    
SetVars.do_it(None)


username = os.getenv('SPOTIPY_USER_ID')
scope = 'user-library-read'

token = util.prompt_for_user_token(username, scope)

sp = spotipy.Spotify(auth=token)

