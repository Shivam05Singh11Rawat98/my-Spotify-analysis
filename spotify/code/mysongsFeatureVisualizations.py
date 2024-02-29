import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import calplot
import calmap

#####################################
from autoviz import AutoViz_Class
AV = AutoViz_Class()

filename = "uniqueTracks.csv"
target_variable = "valence"

dft = AV.AutoViz(
    filename,
    sep=",",
    depVar=target_variable,
    dfte=None,
    header=0,
    verbose=1,
    lowess=False,
    chart_format="svg",
    max_rows_analyzed=150000,
    max_cols_analyzed=30,
    save_plot_dir=None
)


#####################################

sns.set_style("darkgrid")

unique_tracks = pd.read_csv("uniqueTracks.csv", encoding='latin1')
unique_tracks.head(10)

unique_tracks = unique_tracks.drop(columns=['Unnamed: 0'])
unique_tracks.head(10)

small = unique_tracks[['danceability', 'energy', 'speechiness', 'acousticness', 'liveness', 'valence']]
plt.figure(figsize=(10,4))
small.mean().plot.bar()
plt.title('Mean Values of Audio Features')
plt.show()

features = ['danceability', 'energy', 'key', 'loudness' ,'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence','tempo']

# plotting histogram for each feature
for col in features:
  sns.displot(unique_tracks, x=col, kde=True)
  plt.show()
  
  
sns.countplot(data=unique_tracks, x='key', hue='mode', palette = 'Set3')


#Correlation processing
unique_tracks_small = unique_tracks[['danceability', 'energy', 'speechiness','mode', 'acousticness', 'liveness', 'valence']]
mask = np.triu(np.ones_like(unique_tracks_small.corr(), dtype=bool))

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 8))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(230, 20, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(unique_tracks_small.corr(), mask=mask, cmap=cmap, vmin=-1, vmax=1, 
            square=True, linewidths=.5, cbar_kws={"shrink": .5})

##############################################################################################
artist_names = ['KK','Arctic Monkeys','Arijit Singh','Atif Aslam','Pink Floyd','Gorillaz']
artist_names.sort()
print(artist_names)
radar = unique_tracks[unique_tracks['artistName'].isin(artist_names)][['artistName','energy', 'danceability', 'valence', 'liveness', 'acousticness']]
artist_radar= radar.groupby('artistName', as_index=False).mean().sort_values('artistName')
artist_radar = artist_radar[['energy', 'danceability', 'valence', 'liveness', 'acousticness']]
artist_radar

def plot_radar(idx,color):
  # categories
  category = ['energy', 'danceability', 'valence', 'liveness', 'acousticness']
  N = len(category)

  #values
  values = artist_radar.iloc[idx].to_list()
  values += values[:1]

  # calculate angle for each category
  angles = [n / float(N) * 2 * np.pi for n in range(N) ]
  angles += angles[:1]

  # plot
  plt.polar(angles, values, marker = '.', color=color)
  plt.fill(angles, values, alpha=0.3, color=color)

  # x labels
  plt.xticks(angles[:-1], category)

  # y labels
  plt.yticks([0.2,0.4,0.6,0.8])
  plt.ylim(0,1)
  
color = ['crimson', 'teal', 'yellowgreen', 'gold', 'maroon', 'green']

plt.rcParams['figure.figsize'] = (30,30)

# for loop to plot all the 9 playlists
for i in range(len(artist_radar)):
  k = i+1
  ax = plt.subplot(int('33' + str(k)), polar='True')
  ax.title.set_text(artist_names[i])
  plot_radar(i,color[i])

plt.show()

