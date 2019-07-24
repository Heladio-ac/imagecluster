#!/usr/bin/python3

# Detailed API example. We show which functions are called inside
# get_image_data() (read_images(), get_model(), fingerprints(), pca(),
# read_timestamps()) and show more options such as time distance scaling.

from imagecluster import calc, io as icio, postproc
from ecosia_images import crawler
from PIL import Image
import sys
import imghdr

##images,fingerprints,timestamps = icio.get_image_data(
##    'pics/',
##    pca_kwds=dict(n_components=0.95),
##    img_kwds=dict(size=(224,224)))

# Create image database in memory. This helps to feed images to the NN model
# quickly.

def search_cluster(keyword):
    directory = 'downloads/%s' % keyword

    print('Starting crawler')

    searcher = crawler()
    try:
        print('Searching for %s' % keyword)
        searcher.search(keyword)
        print('Downloading')
        files = searcher.download(50)
    except:
        searcher.stop()
        sys.exit(0)

    print('Converting pictures into jpg')
    for file in files:
        try:
            if not imghdr.what(file) == 'jpeg':
                im = Image.open(file)
                rgb_im = im.convert('RGB')
                rgb_im.save(file + '.jpg')
        except:
            pass

    images = icio.read_images(directory, size=(224,224))

    # Create Keras NN model.
    model = calc.get_model()

    # Feed images through the model and extract fingerprints (feature vectors).
    print('Feeding images to the neural network')
    fingerprints = calc.fingerprints(images, model)

    # Optionally run a PCA on the fingerprints to compress the dimensions. Use a
    # cumulative explained variance ratio of 0.95.
    fingerprints = calc.pca(fingerprints, n_components=0.95)

    # Read image timestamps. Need that to calculate the time distance, can be used
    # in clustering.
    timestamps = icio.read_timestamps(directory)

    # Run clustering on the fingerprints. Select clusters with similarity index
    # sim=0.5. Mix 80% content distance with 20% timestamp distance (alpha=0.2).
    clusters = calc.cluster(fingerprints, sim=0.5, timestamps=timestamps, alpha=0.2)

    # Create dirs with links to images. Dirs represent the clusters the images
    # belong to.
    postproc.make_links(clusters, directory + '/imagecluster/clusters')

    # Plot images arranged in clusters and save plot.
    fig,ax = postproc.plot_clusters(clusters, images)
    fig.savefig('foo.png')


search_cluster('cart icon')
search_cluster('web icon')
search_cluster('money icon')
search_cluster('login icon')
