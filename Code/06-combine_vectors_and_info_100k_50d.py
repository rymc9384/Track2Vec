# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 12:47:34 2017

@author: rbm166
"""

import pickle 
import pandas as pd
import numpy as np


###################################
### FUNCTIONS:
###################################

##
## 1) Read in the vectors and format them (sourced from GloVe code -- Stanford NLP Group)
## 

def generate(vocab_file,vectors_file):
    
    with open(vocab_file, 'r') as f:
        words = [x.rstrip().split(' ')[0] for x in f.readlines()]
    with open(vectors_file, 'r') as f:
        vectors = {}
        for line in f:
            vals = line.rstrip().split(' ')
            vectors[vals[0]] = [float(x) for x in vals[1:]]

    vocab_size = len(words)
    vocab = {w: idx for idx, w in enumerate(words)}
    ivocab = {idx: w for idx, w in enumerate(words)}

    vector_dim = len(vectors[ivocab[0]])
    W = np.zeros((vocab_size, vector_dim))
    for word, v in vectors.items():
        if word == '<unk>':
            continue
        W[vocab[word], :] = v

    # normalize each word vector to unit variance
    W_norm = np.zeros(W.shape)
    d = (np.sum(W ** 2, 1) ** (0.5))
    W_norm = (W.T / d).T
    return (W_norm, vocab, ivocab)


###################################
### 0) READ IN DATA
###################################

## 0a) Read in the vectors:

vocab_file = 'E:/Users/rbm166/Desktop/GloVe_Spotify/vocab100k_50d.txt'
vectors_file = 'E:/Users/rbm166/Desktop/GloVe_Spotify/vectors100k_50d.txt'

vector, vocab, v_idx = generate(vocab_file,vectors_file)


## 0b) Read in the lookup table:
with open('E:/Users/rbm166/Desktop/GloVe_Spotify/Lookup_Vocab100k_50d.txt', 'rb') as f:
    lookup = pickle.load(f)
    
    

###################################
### 1) PUT INTO DATAFRAMES
###################################

## 1a) Lookup Table dataframe:
df_lookup = pd.DataFrame.from_dict(data=lookup,orient='index')


## 1b) Vectors dataframe:
vector_dict = {}
for v in range(len(v_idx)):
    vector_dict[v_idx[v]] = vector[v]
    
df_vect = pd.DataFrame.from_dict(data=vector_dict,orient='index')

## 1c) Join the two dataframes:
df_final = df_lookup.join(other=df_vect,how='right')


## 1d) Put in the frequency values for the "filler" words ('ROOT', 'END', & 'DUMMY'):
df_final.set_value('ROOT','freq',100016)
df_final.set_value('END','freq',100016)
df_final.set_value('DUMMY','freq',500080)

# NOTE: Values come from the "GloVe vocab100k_50d.txt" file, just didn't want 
#       to read the lines in.


###################################
### 2) Write out to CSV:
###################################
df_final.to_csv('../Data/01-vectors_lookup_combined100k_50d.csv')


