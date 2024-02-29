import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import calplot
import calmap

sns.set_style("darkgrid")

streaminData = pd.read_csv("myStreamingData.csv", encoding='latin1')
streaminData.head(10)

streaminData.columns

streaminData = streaminData.drop(columns=['Unnamed: 0.1','Unnamed: 0', 'name', 'type', 'uri', 'track_href', 'analysis_url', 'duration_ms' ])
streaminData.describe()

# converting ms to minute and extracting date from datetime column
streaminData['mins_played'] = streaminData.apply(lambda x: round(x['msPlayed']/60000,2), axis=1)
streaminData['date'] = streaminData.apply(lambda x: pd.to_datetime(x['endTime'][:10],format='%Y-%m-%d'),axis=1)
min(streaminData['date'])

from datetime import datetime

date_str = '2023-10-31'

date_object = datetime.strptime(date_str, '%Y-%m-%d').date()

# calculate the daily streaming time length 
dailyLength = streaminData.groupby('date', as_index=False).sum()
dailyLength.head(10)

# create new date series for displaying time series data
idx = pd.DataFrame(pd.date_range(date_object, max(streaminData.date)),columns=['date'])
idx['date'] = idx.apply(lambda x: pd.to_datetime(x['date'],format='%Y-%m-%d'),axis=1)

idx.head(10)

# use new date series to display the daily streaming time
new_daily_length = pd.merge(idx, dailyLength, how='left', on='date', copy=False)
new_daily_length
# getting rid of columns except for date and time
new_daily_length = new_daily_length.drop(new_daily_length.loc[:, 'msPlayed':'time_signature'], axis=1)

# setting date as index
new_daily_length.index = new_daily_length.date

new_daily_length = new_daily_length.drop(columns=['date'])



# converting the dataframe into series for calplot
beta_new_daily_length = new_daily_length['mins_played']
beta_new_daily_length

calplot.calplot(beta_new_daily_length, figsize=(20,10), suptitle='My Streaming History', cmap='Spectral' )

#####################################################################################################################

#getting no. of unique songs and streamed mins of every artist
streaminData.columns
artist_song_cnt = streaminData.groupby('artistName',as_index=False).agg({'trackName': 'nunique'})
artist_song_cnt.rename(columns={'trackName':'song_count'},inplace=True)
artist_song_cnt.head(10)

my_columns = ['danceability', 'energy', 'loudness', 'mode', 'speechiness',
       'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'artistName', 'trackName', 'mins_played']

artist_mins_played = streaminData[my_columns].groupby('artistName',as_index=False).sum()
artist_mins_played.head(10)

artist_streaming_data = pd.merge(artist_mins_played,artist_song_cnt, how='left', on='artistName')
artist_streaming_data.head(10)

artist_streaming_data.drop(artist_streaming_data[artist_streaming_data['artistName'] == 'The Ranveer Show'].index, inplace=True)

most_heard_30 = artist_streaming_data.sort_values('mins_played', inplace=False, ascending=False).head(30)

most_heard_30['artistName'].head(1)

# barplot artist vs minutes_played
plt.rcParams["figure.figsize"] = (20,20)
sns.barplot(y = most_heard_30['artistName'], x = most_heard_30['mins_played'], palette='rocket_r')
plt.title('Top 30 Artist heard')
plt.show()

# converted df to dict
artist_freq = dict(zip(artist_streaming_data['artistName'].tolist(), artist_streaming_data['mins_played'].tolist()))
artist_by_song_cnt = dict(zip(artist_streaming_data['artistName'].tolist(), artist_streaming_data['song_count'].tolist()))
# import wordcloud
from wordcloud import WordCloud

# plot wordcloud
wc = WordCloud(background_color='black',width=800, height=400, max_words=100).generate_from_frequencies(artist_freq)
plt.figure(figsize=(20, 10))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.show()

#barplot to showcase the song freq for top 50 artist by the count
max_songs = artist_streaming_data.sort_values('song_count', inplace=False, ascending=False).head(50)
sns.barplot(y = max_songs['artistName'], x = max_songs['song_count'], palette='summer')
plt.rcParams["figure.figsize"] = (20,20)

#mood throughout during the listning period
valence = streaminData.groupby('date')['valence'].aggregate(['min', np.mean, 'max'])
val = pd.merge(idx, valence, how='left', left_on='date', right_on = 'date', copy=False).fillna(0)

plt.rcParams["figure.figsize"] = (30,10)
plt.errorbar(val["date"],val["mean"], [val["mean"] - val['min'],val['max']-val["mean"]], linestyle='None',marker='^')
plt.show()

#plot for more than one y feature



#
small = streaminData[['danceability', 'energy', 'speechiness', 'acousticness', 'liveness', 'valence']]
plt.figure(figsize=(10,4))
small.mean().plot.bar()
plt.title('Mean Values of Audio Features')
plt.show()
streaminData.shape