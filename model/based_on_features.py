import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.neighbors import NearestNeighbors
dataframe=pd.read_csv("dataset.csv")
dataframe=dataframe.drop(['duration_ms','popularity','album_name','time_signature','track_genre','Unnamed: 0', 'mode'],axis=1)
dataframe.drop_duplicates(subset=['track_id'],inplace=True)
dataframe=dataframe.drop(['track_id'],axis=1)
dataframe.dropna()
dataframe.reset_index()
scaler=preprocessing.MinMaxScaler()
names=dataframe.select_dtypes(include=np.number).columns
d=scaler.fit_transform(dataframe.select_dtypes(include=np.number))
nn=NearestNeighbors(n_neighbors=5)
nn.fit(d)
def recommend(song,artist):
    i=dataframe[dataframe['artists']==artist]
    i=i[i['track_name']==song]
    inum=scaler.fit_transform(i.select_dtypes(include=np.number))
    neigh=nn.kneighbors(inum,return_distance=False)[0]
    art_song={} 
    song=dataframe['track_name'].iloc[neigh].tolist()
    art=dataframe['artists'].iloc[neigh].tolist()
    for i in range(len(song)):
        art_song[song[i]]=art[i]
    return art_song
artist=input("Artist Name")
song=input("Song Name")
recommend(song,artist)