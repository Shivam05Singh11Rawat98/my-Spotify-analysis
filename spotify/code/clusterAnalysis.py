import pandas as pd
import numpy as np
from matplotlib import rcParams
import seaborn as sns
import matplotlib.pyplot as plt




#reading track_2Dset
tracks = pd.read_csv('myStreamingtrack_2D.csv')
#tracks.head(10)

#dropping unwanted columns
tracks = tracks.drop(columns=['Unnamed: 0', 'Unnamed: 0.1', 'endTime', 'id'])
# tracks.head(10)

# taking required columns
tracks_new = tracks[['danceability','energy','loudness','speechiness','acousticness','instrumentalness','liveness','valence','tempo']]

#scaling track_2D
from sklearn import preprocessing
tracks_scaled = preprocessing.scale(tracks_new)
tracks_scaled


from sklearn.manifold import TSNE
tracks_tsne = TSNE(learning_rate=100).fit_transform(tracks_scaled)

track_2D = pd.track_2DFrame({'d1': tracks_tsne[:, 0], 'd2': tracks_tsne[:, 1]})

rcParams['figure.figsize'] = 20,8
sns.scatterplot(x=tracks_tsne[:, 0], y=tracks_tsne[:, 1])

#elbow to get the no. of clusters
from sklearn.cluster import KMeans

wcss = []

for i in range(1,15):
    kmeans = KMeans(i)
    kmeans.fit(tracks_scaled)
    wcss.append(kmeans.inertia_)
    
wcss
    
plt.plot(range(1, 15), wcss, marker='o')
plt.title('Elbow Method')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Within Cluster Sum of Squares (WCSS)')
plt.show()


kmeans_model = KMeans(8)
kmeans_model.fit(tracks_scaled)
track_2D['kmeans']=kmeans_model.fit_predict(tracks_scaled)

rcParams['figure.figsize'] = 18,8
sns.scatterplot(track_2D=track_2D, x='d1', y='d2', hue='kmeans', palette='nipy_spectral')


from sklearn.cluster import AgglomerativeClustering

# agglomerative
model_agg = AgglomerativeClustering(n_clusters=6)
model_agg.fit(tracks_scaled)
track_2D['agg']=model_agg.fit_predict(tracks_scaled)

# plotting
rcParams['figure.figsize'] = 18,8
sns.scatterplot(data=track_2D, x='d1', y='d2', hue='agg', palette='viridis')