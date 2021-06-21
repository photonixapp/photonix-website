# Image Analysis

This aims to detail the technical implementation of the image analysis and AI models included in Photonix.


## Color Analysis

The aim of this model is to say how much of an image is close to a pre-defined palette. This code is located at [`photonix/classifiers/color/model.py`](https://github.com/photonixapp/photonix/blob/master/photonix/classifiers/color/model.py).

A set of colour names and their RGB values are pre-defined in the model code.

Each image being analysed gets resampled (scaled) to 32 × 32 pixels using the bicubic algorithm included in [Pillow](https://python-pillow.org/).

A function `color_distance` takes two RGB values and returns a score for how different they are. It does this by first converting to the [HSV color space](https://en.wikipedia.org/wiki/HSL_and_HSV) as this maps more closely to the color spectrum that humans are familiar with. This conversion is done using the `rgb_to_hsv` function of the `colorsys` Python standard library module. The difference of each the Hue, Saturation and Value are calculated and multiplied together. The Hue is given more of a weighting as it is deemed more important.

Each of the 1024 total pixels in the image are compared to each of the pre-defined colors using the `color_distance` function explained above. The color that is the closest match gets an incremented count — basically building up a histogram. The counts get divided by the number of pixels to get scalar values adding up to 1.0.

Only the names and scores of colors that received a match are returned and they are sorted from most frequent to least. There is a minimum score threshold that must be met or it will not show in the output. This eliminates outliers. Because of this, the scores for each of the color buckets may not sum up to 1.0.


## Location Detection

The aim of this model is to extract GPS coordinates from an image and return two things — the name of the country the photo was taken in and the name of the town/city. This code is located at [`photonix/classifiers/location/model.py`](https://github.com/photonixapp/photonix/blob/master/photonix/classifiers/location/model.py).

We provide two data sources so that all processing can be done locally and quickly — no APIs need to be called. The data sources are:

- [World Borders Dataset from thematicmapping.org](http://thematicmapping.org/downloads/world_borders.php) (Creative Commons Attribution-Share Alike License). This contains a [shapefile](https://en.wikipedia.org/wiki/Shapefile) of all the countries.
- [GeoNames Top 1000 cities](http://download.geonames.org/export/dump/) (Creative Commons Attribution 4.0 International License). This contains latitudes and longitudes for the 1000 most populated cities in the world.

### Country

We first load the countries shapefile using the pure Python library [pyshp](https://github.com/GeospatialPython/pyshp). We then loop over each country and load it's polygon into [matplotlib's path module](https://matplotlib.org/3.1.0/api/path_api.html). We can then use a convenient function from the module `contains_points` to determine if our photo's location is within the country's border.

One notable point is that the country polygons are not particularly detailed. Currently it works well if the photo is taken inland but photos taken on beaches can sometimes miss out. A future enhancement would be to broaden the search radius (within reason) to try and get within the nearest country's border. A more detailed shapefile of countries could also be procured but the extra points could really slow things down.

### City

This is much simpler than the calculation for country. We loop over all cities in our list and calculate the distance between it and our photo's coordinates using the [`haversine`](https://en.wikipedia.org/wiki/Haversine_formula) function. This is fairly simplistic as it assumes a spherical world and doesn't account for terrain but is good enough (and fast enough) for our use case. We exclude any cities that have a distance over 10km and return the nearest one (if any).


## Style Classification

Details coming soon.

## Object Recognition

Details coming soon.

## Face Detection and Recognition

This model was completed in June 2021. There are a few different steps to the process. Facial recognition is different from our other types of analysis as it only becomes useful if the user can label the people they know. Because of this, part of the model is automatically re-trained to apply the user's own face labels.

Papers With Code provides [benchmark comparisons of algorithms](https://paperswithcode.com/area/computer-vision/facial-recognition-and-modelling) for each step (and more).

### Face Detection

We use a Convolutional Neural Network (CNN) called "Multi-task Cascaded Convolutional Network" (MTCNN) which is specialised in identifying faces in photos and features such as eyes, nose and mouth. You can find more details in the paper [Joint Face Detection and Alignment using Multi-task Cascaded Convolutional Networks](https://arxiv.org/pdf/1604.02878.pdf) written by Zhang, K et al. (2016) [ZHANG2016]. You can also see some examples images of what's detected at [the author's site](https://kpzhang93.github.io/SPL/index.html).

We use a modified version of a Python package called [mtcnn](https://github.com/ipazc/mtcnn) by Iván de Paz Centeno. This implementation suited us as it was based around Keras and the Tensorflow framework. It also included a pre-trained weights file which we use out-of-the box. Our modifications were to replace the use of OpenCV with Pillow for image scaling operations. This saved space as we already already had Pillow installed for other areas of the application.

The bounding box output of running this model against photos is used to create location-specific tags in the database. These tags are of unknown people at this stage but it's still useful to tag the information in the database at this step.

### Face Alignment / Transformation and Cropping

Because faces can be oriented and pointing in different directions we want to normalise them as much as possible. We apply skew and rotate transformations to face images to align all the eyes, nose and mouths consistently. The code we use for this step comes from the [Deepface](https://github.com/serengil/deepface/) library by Sefik Ilkin Serengil (not to be confused with Facebook's DeepFace neural network architecture from 2014).

### Feature Extraction / Embedding / Face Fingerprinting / Faceprinting

Several Deep Neural Networks (DNNs) exist which can generate a multi-dimensional representation of each face. FaceNet is one of the more famous examples. Papers With Code provides a [list of models sorted by accuracy](https://paperswithcode.com/sota/face-verification-on-labeled-faces-in-the).

This is the model we chose to use as it was the best performing implementation included in the [Deepface](https://github.com/serengil/deepface/) library. We can compare it to others in future if they are noticeably better but FaceNet is quite performant, battle tested and produces output embeddings of a reasonable size. It is assumed that Google Photos is currently using FaceNet.

When provided with a photo of a face, the neural network outputs an embedding vector (array) of 128 floating point values. You can think of these as features of the face such as width of mouth and together they make up a kind of fingerprint.

The embedding of a face image only needs to be computed once and then it gets saved against the face tag in the database, ready for the next step.

### Similarity Calculation / Clustering / Classification

The face embeddings (or fingerprints) have been generated and saved but no two photos of the same face will match exactly. There are always slight variations caused by things like lighting, orientation, emotion and hair. We can however calculate how similar one embedding is to another using a distance formula. The recommended formula for FaceNet is the [Euclidean distance](https://en.wikipedia.org/wiki/Euclidean_distance) which can compare all 128 dimensions of our embedding and give us a single number as a result.

A threshold is decided upon and if the Euclidean distance of two face embeddings is below this value then we assume the photos to be of the same person.

Computing the distance between two embeddings is quite fast but as more and more photos of faces are added to your library the number of comparisons you would have to do between them increases exponentially. To solve this issue we implement an ANN (Approximate [Nearest Neighbors](https://en.wikipedia.org/wiki/Nearest_neighbor_search)) search index using the [Annoy](https://github.com/spotify/annoy) library. This is what Spotify uses to suggest similar songs you might like and it is able to do this for every user, every day across its entire library of tracks.

The ANN is fast to generate and is re-created at 5-minutely intervals if new face tags have been added since last generation. A hybrid approach is used whereby any face tags added since last index generation are compared individually. This means that similar face photos imported within a short period of time will still match (it just takes a bit longer until the index catches up).

### Labelling

An interesting point to note is that similar faces can be grouped together even if we don't know who the person is. Because of this, if a face photo isn't similar enough to a face labelled by the user we create a random tag name in the form "Unknown person 123456" where the number is random. Grouping happens while photos are imported and the user just has to go and change the tag name to the person they know.

We are slightly cautious while we are grouping faces together as it is much easier for a user to merge two groups that are actually the same rather than having to remove faces from a group.

Our user interface shows bounding boxes for faces and allows quick approval, rejection and editing of automatic face tags.
