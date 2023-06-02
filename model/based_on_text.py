import os
import sys
import json
import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors


# sys.stdout = open('/dev/null', 'w')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def preprocessing():

    
    # with tf.device('/device:GPU:0'):
        df = pd.read_csv('/Users/mudittyagi/Coding/PRACTICUM/data/lyrics.csv')
        df.reset_index()
        model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
        # model = hub.load("https://tfhub.dev/google/universal-sentence-encoder-lite/2")

        def create_embed(texts):
            batch_size = 1024 
            # Adjust the batch size as needed
            embeddings = []
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i+batch_size]
                embeddings.append(model(batch))
            return tf.concat(embeddings, axis=0)

        lyrics = list(df['text'])
        # lyrics = lyrics[:10000]  
        # Adjust the number of lyrics as needed
        emb = create_embed(lyrics)

        nn = NearestNeighbors(n_neighbors=5)
        nn.fit(emb)

        def recommend(text):
            textemb=create_embed([text])
            neighbors=nn.kneighbors(textemb,return_distance=False)[0]
            artist=[]
            tracks=[]
            
            artist.append(df['artist'].iloc[neighbors].to_list())
            tracks.append(df['song'].iloc[neighbors].to_list())

            artist = artist[0]
            tracks = tracks[0]
            # print(artist) 
            # print(tracks)

            result = {'artist':artist, 'tracks':tracks}
            print(json.dumps(result))

        recommend(sys.argv[1])

preprocessing()
# print(sys.argv[1])