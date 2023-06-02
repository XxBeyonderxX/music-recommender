import sys
import json
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
# import langid

# dataframe = pd.read_csv("/Users/mudittyagi/Coding/PRACTICUM/data/features.csv")

# dataframe = dataframe.drop(['duration_ms','popularity','album_name','time_signature','track_genre','Unnamed: 0', 'mode'],axis=1)
# dataframe.drop_duplicates(subset=['track_id'],inplace=True)
# dataframe.drop_duplicates(subset=['track_name'],inplace=True)
# dataframe.drop_duplicates(subset=['artists', 'track_name'],inplace=True)
# dataframe = dataframe.drop(['track_id'],axis=1)

# dataframe.dropna(inplace=True)
# dataframe.reset_index(inplace=True)

# dataframe = dataframe[~dataframe['artists'].fillna('').str.contains(';')]

# dataframe['artists'] = dataframe['artists'].str.split(';').str[0]

# #chinese rows removed
# dataframe = dataframe[~dataframe['track_name'].str.contains(r'[\u4e00-\u9fff]')]

# #non ascii alphabets removed
# dataframe = dataframe[~dataframe['track_name'].str.contains(r'[^\x00-\x7F]+', regex=True)]
# dataframe = dataframe[~dataframe['artists'].str.contains(r'[^\x00-\x7F]+', regex=True)]

# #non english tracks removed
# dataframe = dataframe[dataframe['track_name'].apply(lambda x: langid.classify(str(x))[0] == 'en')]

# dataframe.to_csv('/Users/mudittyagi/Coding/PRACTICUM/data/features2.csv', index=False)
dataframe = pd.read_csv("/Users/mudittyagi/Coding/PRACTICUM/data/features2.csv")

# duplicates = dataframe['track_name'].duplicated()
# print(duplicates.sum())

dataframe['artists'] = dataframe['artists'].str.lower()
dataframe['track_name'] = dataframe['track_name'].str.lower()

scaler = MinMaxScaler()
names = dataframe.select_dtypes(include=np.number).columns
d = scaler.fit_transform(dataframe.select_dtypes(include=np.number))

nn = NearestNeighbors(n_neighbors=6)
nn.fit(d)

def recommend(track):
    
    # i=dataframe[dataframe['artists']==artist]
    # i=i[i['track_name']==track]

    # row = dataframe[(dataframe['artists'] == artist) & (dataframe['track_name'] == track)]
    row = dataframe[(dataframe['track_name'] == track)]
    # print(row)    
    
    filtered_features = scaler.transform(row.select_dtypes(include=np.number))
    # print(filtered_features)

    # inum = scaler.fit_transform(i.select_dtypes(include=np.number))
    
    neigh = nn.kneighbors(filtered_features, return_distance=False)[0]

    tracks = dataframe['track_name'].iloc[neigh[1:]].tolist()
    artist = dataframe['artists'].iloc[neigh[1:]].tolist()
    # print(tracks)
    # print(artist)

    result = { 'artist': artist, 'tracks': tracks }
    print(json.dumps(result))
    

# artist=input("Artist Name")
# song=input("Song Name")
# recommend(song,artist)


# recommend("I'm Yours", 'Jason Mraz')
# recommend("Facts of Life", 'Jeff Foxworthy')

# recommend("Hold On")
recommend (sys.argv[1])