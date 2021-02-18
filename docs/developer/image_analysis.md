# Image Analysis

This aims to detail the technical implementation of the image analysis and AI models included in Photonix.


## Color Analysis

The aim of this model is to say how much of an image is close to a pre-defined palette. This code is located at [`photonix/classifiers/color/model.py`](https://github.com/damianmoore/photonix/blob/master/photonix/classifiers/color/model.py).

A set of colour names and their RGB values are pre-defined in the model code.

Each image being analysed gets resampled (scaled) to 32 × 32 pixels using the bicubic algorithm included in [Pillow](https://python-pillow.org/).

A function `color_distance` takes two RGB values and returns a score for how different they are. It does this by first converting to the [HSV color space](https://en.wikipedia.org/wiki/HSL_and_HSV) as this maps more closely to the color spectrum that humans are familiar with. This conversion is done using the `rgb_to_hsv` function of the `colorsys` Python standard library module. The difference of each the Hue, Saturation and Value are calculated and multiplied together. The Hue is given more of a weighting as it is deemed more important.

Each of the 1024 total pixels in the image are compared to each of the pre-defined colors using the `color_distance` function explained above. The color that is the closest match gets an incremented count — basically building up a histogram. The counts get divided by the number of pixels to get scalar values adding up to 1.0.

Only the names and scores of colors that received a match are returned and they are sorted from most frequent to least. There is a minimum score threshold that must be met or it will not show in the output. This eliminates outliers. Because of this, the scores for each of the color buckets may not sum up to 1.0.


## Location Detection

The aim of this model is to extract GPS coordinates from an image and return two things — the name of the country the photo was taken in and the name of the town/city. This code is located at [`photonix/classifiers/location/model.py`](https://github.com/damianmoore/photonix/blob/master/photonix/classifiers/location/model.py).

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

This collection of models is currently being developed. There are a few different steps to the process. Facial recognition is different from most of the other types of analysis as it only becomes useful if the user can label the people they know. Because of this, parts of the model need to be re-trained when there is new data and then run against the detected, unknown faces.

Papers With Code provides [benchmark comparisons of algorithms](https://paperswithcode.com/area/computer-vision/facial-recognition-and-modelling) for each step (and more).

### Face Detection

We use a Convolutional Neural Network (CNN) called "Multi-task Cascaded Convolutional Network" (MTCNN) which is specialised in identifying faces in photos and features such as eyes, nose and mouth. You can find more details in the paper [Joint Face Detection and Alignment using Multi-task Cascaded Convolutional Networks](https://arxiv.org/pdf/1604.02878.pdf) written by Zhang, K et al. (2016) [ZHANG2016]. You can also see some examples images of what's detected at [the author's site](https://kpzhang93.github.io/SPL/index.html).

We use a modified version of a Python package called [mtcnn](https://github.com/ipazc/mtcnn) by Iván de Paz Centeno. This implementation suited us as it was based around Keras and the Tensorflow framework. It also included a pre-trained weights file which we use out-of-the box. Our modifications were to replace the use of OpenCV with Pillow for image scaling operations. This saved space as we already already had Pillow installed for other areas of the application.

The bounding box output of running this model against photos is used to create location-specific tags in the database. These tags are of unknown people at this stage but it's still useful to tag the information at this stage.

### Face Alignment / Transformation and Cropping

Because faces can be oriented and pointing in different directions we want to normalise them as much as possible. We will skew and rotate the face images to align all the eyes, nose and mouths consistently.

The output images from this step can be cached for later steps.

### Feature Extraction / Embedding / Face Fingerprinting / Faceprinting

Several Deep Neural Networks (DNNs) exist which can generate a multi-dimensional representation of each face. FaceNet is one of the more famous examples. Papers With Code provides a [list of models sorted by accuracy](https://paperswithcode.com/sota/face-verification-on-labeled-faces-in-the).

The outputted embeddings only need to be computed once to be re-used many times in the final re-training step.

### Similarity Calculation / Clustering / Classification

This model will be computing which faces are most similar to each other. If an unknown face has a distance score within a defined threshold to it's nearest neighbour, it will get labelled.

The technique used here doesn't apparently matter too much. It can be something like an SVM which can be very quick to re-train and infer.
