import tensorflow as tf
import tensorflow_hub as hub
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
df=pd.read_csv("spotify_millsongdata.csv")
df.reset_index()
model=hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
def create_embed(df):
        return model(df)
lyrics=list(df['text'])
lyrics=lyrics[:5000]
emb=create_embed(lyrics)
nn=NearestNeighbors(n_neighbors=5)
nn.fit(emb)
def recommend(text):
    textemb=create_embed([text])
    neighbors=nn.kneighbors(textemb,return_distance=False)[0]
    art=df['artist'].iloc[neighbors].tolist()
    song=df['song'].iloc[neighbors].tolist()
    art_song={}
    for i in range(len(art)):
        art_song[song[i]]=art[i]
    return art_song
text=input("Search ")
recommend(text)