import sys
import json
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer

def preprocessing():
    df = pd.read_csv("/Users/mudittyagi/Coding/PRACTICUM/data/topic.csv")
    # df = df.head(20000)
    df.drop_duplicates(subset=["track_name"], inplace=True)
    df.rename(columns={df.columns[0]: 's_no'}, inplace=True)

    df['lyrics'] = df['lyrics'].apply(lambda x:x.split())
    df['artist_name'] = df['artist_name'].apply(lambda x:x.split())
    df['track_name'] = df['track_name'].apply(lambda x:x.split())
    df['genre'] = df['genre'].apply(lambda x:x.split())
    df['topic'] = df['topic'].apply(lambda x:x.split())

    # df['combined'] = df['artist_name'] + df['track_name'] + df['genre'] + df['topic'] + df['lyrics']
    df['combined'] = df['artist_name'] + df['track_name'] + df['topic']

    df['combined'] = df['combined'].apply(lambda x:" ".join(x))

    ps = PorterStemmer()

    def stem(text):
        y=[]
        for i in text.split():
            y.append(ps.stem(i))
    
        return " ".join(y)

    df['combined'] = df['combined'].apply(stem)
    
    cv = CountVectorizer(max_features=400, stop_words='english')
    vectors = cv.fit_transform(df['combined']).toarray()

    similarity = cosine_similarity(vectors)
    return df, similarity

def recommend(track):
    df, similarity = preprocessing()

    df['track_name'] = df['track_name'].apply(lambda x:" ".join(x))
    df['artist_name'] = df['artist_name'].apply(lambda x:" ".join(x))

    # print('preprocessing done with input : ', sys.argv[1], similarity.shape, df['track_name'][0])


    track_index = df[df['track_name'] == track].index[0]
    # print('track index', track_index)

    distances = similarity[track_index]
    songs = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]
    
    artist=[]
    tracks=[]

    for i in songs:
        # print(df.iloc[i[0]].artist_name + "  -  " +df.iloc[i[0]].track_name) 
        artist.append(df.iloc[i[0]].artist_name)
        tracks.append(df.iloc[i[0]].track_name)
    
    result = {'artist':artist, 'tracks':tracks}
    print(json.dumps(result))

recommend(sys.argv[1])