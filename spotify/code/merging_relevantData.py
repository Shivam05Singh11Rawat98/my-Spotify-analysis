import pandas as pd
import json

with open('../MyData/StreamingHistory0.json') as f:
    data = json.load(f)
    
print(data)

df = pd.json_normalize(data)
df.head(10)

streaming_history = pd.read_csv('streaming_history.csv')
streaming_history.head(10)


streaming_data = pd.merge(streaming_history,df, how='left',left_on='name' ,right_on='trackName')
streaming_data.head(10)

streaming_data.shape

streaming_data.drop_duplicates(keep='first', inplace=True)
streaming_data.head(10)
streaming_data.shape

streaming_data.to_csv('myStreamingData.csv')


track_features = ['trackName','artistName' ,'danceability', 'energy', 'key', 'loudness' ,'speechiness', 'acousticness','mode', 'instrumentalness', 'liveness', 'valence','tempo']
unique_track_features = streaming_data.drop_duplicates('trackName',inplace=False)[track_features]
unique_track_features.head(10)

unique_track_features.to_csv('uniqueTracks.csv', index=False)