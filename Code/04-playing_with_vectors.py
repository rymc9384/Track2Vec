# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 14:03:50 2017

@author: rbm166
"""

import pickle
import os
import numpy as np

## FUNCTIONS 
# Sourced 

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



def distance(W, vocab, ivocab, input_term):
    for idx, term in enumerate(input_term.split(' ')):
        if term in vocab:
            print('Word: %s  Position in vocabulary: %i' % (term, vocab[term]))
            if idx == 0:
                vec_result = np.copy(W[vocab[term], :])
            else:
                vec_result += W[vocab[term], :] 
        else:
            print('Word: %s  Out of dictionary!\n' % term)
            return
    
    vec_norm = np.zeros(vec_result.shape)
    d = (np.sum(vec_result ** 2,) ** (0.5))
    vec_norm = (vec_result.T / d).T

    dist = np.dot(W, vec_norm.T)

    for term in input_term.split(' '):
        index = vocab[term]
        dist[index] = -np.Inf

    a = np.argsort(-dist)[:N]

    out = []
    print("\n                               Word       Cosine distance\n")
    print("---------------------------------------------------------\n")
    for x in a:
        print("%35s\t\t%f\n" % (ivocab[x], dist[x]))
        out.append((ivocab[x], dist[x]))
        
    return(out)


## LOAD THE LOOKUP TABLE:
with open('..\Data\TrackID_Lookup.txt', 'rb') as f:
    tab = pickle.load(f)
    
keys = list(tab.keys())

    


## LOAD VECTORS: 
    
vocab_file = 'E:/Users/rbm166/Desktop/GloVe_Spotify/vocab.txt'
vectors_file = 'E:/Users/rbm166/Desktop/GloVe_Spotify/vectors.txt'


vector, vocab, v_idx = generate(vocab_file,vectors_file)


## GET THE 50 TRACKS CLOSEST TO 'Heathens' by Twenty One Pilots:
N = 50
heathens = '6i0V12jOa3mr6uu4WYhUBr'

heathens_dist = distance(W=vector,vocab=vocab,ivocab=v_idx,input_term=heathens)

tab['4MsazbPCa0E1MZ5LJmpuQC'] # Good Girl Gone Bad - Rihanna (# 3)
tab['3IiP7JRv3Ew9YJHSLaUKaC'] # Mammoth (radio edit) - Dimitri Vegas et al (# 5)
tab['68DhYEOLtta8k5xug4gVMW'] # Plastic Promises - Set It Off (# 6)
tab['4EWteKXHtcqLhwy4kb1vft'] # Wave From Me - TFLM (# 7)



## GET THE 50 TRACKS CLOSEST TO 'Low Life' (feat The WEEKND) by Future:
lowlife = '7EiZI6JVHllARrX9PUvAdX'

lowlife_dist = distance(W=vector,vocab=vocab,ivocab=v_idx,input_term=lowlife)

tab['4gmmRb6bZJffOOiww1JGTO'] # No Heart - 21 Savage (# 1) -- next song on album is featuring FUTURE
tab['5vkP5g6r7UeKDPeqpgCl9X'] # Trap House - Don Mega & Lil Durk (# 2) -- very similar
tab['6kCP4XiMpWOdBcw010cDdp'] # '#WCW' - Devvon Terrell (# 3) -- another singing rapper
tab['3cCxoOgfi6hgt8MNteuiiD'] # Fade - Kanye West (# 4) -- same kind of autotune
tab['062qh9OokAJELidbTxVSba'] # Ridin' Around - DJ Mustard/ Nipsey Hussle (# 5)
tab['2tbvAGoLMQgjvfgW7naBiE'] # El Chapo - The Game/Skrillex (# 6) -- one of my personal favorites
tab['2nfk39zI8oIdQ7hedtOJDu'] # See Me Fall (feat. Kensei Abbot) - Ro Ransom (# 7) -- another slow singing rap
tab['79NNAu4BprZ1E1ei89Qjdy'] # Dudley Boyz - Westside Gunn (# 8)
tab['0vgtBFdPTkZwQ2gmFu7Dra'] # Figure it Out (feat Kanye West & Nas) - French Montana (# 9) -- slow rap w/ autotuning
tab['6Mbke77AYOB6f4E8axOlMd'] # 4 Real (feat Lil Yachty) - Famous Dex (# 10) -- lots of chorus repetition


## GET THE 50 TRACKS CLOSEST TO 'Cruise' by Florida Georgia Line:
cruise = '0i5el041vd6nxrGEU8QRxy'

cruise_dist = distance(W=vector,vocab=vocab,ivocab=v_idx,input_term=cruise)
tab['5j4hSQH0KaAc8f6cimnXIT'] # Fire Away - Chris Stapleton (# 1) -- slower, but still country
tab['4u7KjVIQPdzGCcAwg4W5Kl'] # Who I Am With You - Chris Young (# 2) -- country, love song
tab['27v7vkeyOlJWxwxY082o9N'] # I Don't Wanna Be Your Friend - Scott McCreary (# 3) -- country love song
tab['04ckx0538IecRehEo1myDh'] # 'The Tin Man - New Version' - Kenny Chesney (# 4)
tab['6hbwFerDj55bMGZZvcInze'] # Bottoms Up (feat. T.I.) - Brantley Gilbert (# 5) -- new age country
tab['4b5Z76krusEOdN1zUusfQN'] # Doin' What She Likes - Blake Shelton (# 6) -- country love song
tab['4w9LtJn74XQhsHD1zAHnzY'] # Show You Off - Dan + Shay (# 7) -- new age country love song
tab[cruise_dist[7][0]]        # Carolina Can - Chase Rice (# 8) -- new country
tab[cruise_dist[8][0]]        # Outta My Head - Craig Campbell (# 9) -- new country love song
tab[cruise_dist[9][0]]        # Hey Girl - Billy Currington (# 10) -- new country love song


## GET THE 50 TRACKS CLOSEST TO 'Goosebumps' by Travis Scott:
goosebumps = '6gBFPUFcJLzWGx4lenP6h2'

goose_dist = distance(W=vector,vocab=vocab,ivocab=v_idx,input_term=goosebumps)
tab[goose_dist[0][0]] # Look At Me! - Xxxtentacion (# 1) - rap w/ electronic background
tab[goose_dist[1][0]] # N.I.N.A. - Tory Lanez (# 2) 
tab[goose_dist[2][0]] # Amansworld - Klangstof (# 3) - not the right genre, but electronic w/ singing
tab[goose_dist[3][0]] # 4 Real - Ty Dolla $ign & ILoveMakonnen (# 4)
tab[goose_dist[4][0]] # Rollin (Bonus Track) - G Herbo (# 5) - harder rap
tab[goose_dist[5][0]] # White Iverson - Post Malone (# 6) - very close in my opinion


# Need U by Elijah Noll
needu = '0008gkpPBkRsRdHTGW27R2'

needu_dist = distance(W=vector,vocab=vocab,ivocab=v_idx,input_term=needu)
tab[needu_dist[0][0]] # Slice & Dice - Dj Guv (# 1) -- Not even close
tab[needu_dist[1][0]] # Christmas Eve - Justin Bieber (# 2) -- much closer
tab[needu_dist[2][0]] # Whip! - Jovanie (# 3) -- not right, but better than the first; another electronic pop song
tab[needu_dist[3][0]] # All For You - Night Riots (# 4) -- close, right genre


# Hands on the Wheel by Schoolboy Q
handson = '2kfpH2OAAdpk5J3JaraAIh'
handson_dist = distance(W=vector,vocab=vocab,ivocab=v_idx,input_term=handson)
tab[handson_dist[0][0]] # Too Many - Russ (# 1) -- close song, and related artist
tab[handson_dist[1][0]] # She (Featuring Frank Ocean) - Tyler the Creator (# 2) -- diff tempo, but related artist and w/ a singing supporting artist
tab[handson_dist[2][0]] # Tamale - Tyler the Creator (# 3) -- similar tempo, again related artist
tab[handson_dist[3][0]] # Tourist (Prod. DJ Khaled) - Travis Scott / Lil Wayne (# 4) -- right genre
tab[handson_dist[4][0]] # She Will (Feat. Drake) - Lil Wayne (# 5) -- right genre, lil wayne again
tab[handson_dist[5][0]] # Bricks (Feat. Migos) - Carnage (# 6) -- iffy
tab[handson_dist[6][0]] # The New Workout Plan - Kanye West (# 7) -- very good match


# Rap God by Eminem
rapgod = '7xB3TwyZMOnKcF50RIXh5b'
rapgod_dist = distance(W=vector,vocab=vocab,ivocab=v_idx,input_term=rapgod)
tab[rapgod_dist[0][0]] # Criminal - Eminem (# 1) -- good pick, same artist
tab[rapgod_dist[1][0]] # Dr. West (Skit) - Eminem (# 2) -- not a song, but same artist 
tab[rapgod_dist[2][0]] # Ooh - Jon Bellion (# 3) -- far off, but actually closer than I thought a Jon Bellion song would be 
tab[rapgod_dist[3][0]] # Stan - Eminem (# 4) -- very good pick
tab[rapgod_dist[4][0]] # See Me (feat. Wiz Khalifa, B.O.B.) - Tech N9ne (# 5) - great pick
tab[rapgod_dist[5][0]] # Gem Shards - MUST DIE! (# 6) -- nope, not really; hard electronic song


