#!/usr/bin/python3

from imagecluster import calc, io as icio, postproc
from ecosia_images import crawler

searcher = crawler(naming='hash')
searcher.search('chilaquiles')
searcher.download(50)

images = icio.read_images('downloads/chilaquiles', size=(224,224))

# Create Keras NN model.
model = calc.get_model()

# Feed images through the model and extract fingerprints (feature vectors).
fingerprints = calc.fingerprints(images, model)

print(fingerprints)

# Optionally run a PCA on the fingerprints to compress the dimensions. Use a
# cumulative explained variance ratio of 0.95.
fingerprints = calc.pca(fingerprints, n_components=0.95)

print(fingerprints)

# Read image timestamps. Need that to calculate the time distance, can be used
# in clustering.
timestamps = icio.read_timestamps('downloads/chilaquiles')

# Run clustering on the fingerprints. Select clusters with similarity index
# sim=0.5. Mix 80% content distance with 20% timestamp distance (alpha=0.2).
clusters = calc.cluster(fingerprints, sim=0.4, timestamps=timestamps, alpha=0.2)
print(clusters)
# Get the size of the biggest cluster
keys = list(clusters.keys())
keys.sort()
key = keys[-1]
print(key)

print(clusters[key][0])
# Create dirs with links to images. Dirs represent the clusters the images
# belong to.
# postproc.make_links(clusters, 'pics/imagecluster/clusters')

# Plot images arranged in clusters and save plot.
fig,ax = postproc.plot_clusters(clusters, images)
# fig.savefig('foo.png')
postproc.plt.show()
