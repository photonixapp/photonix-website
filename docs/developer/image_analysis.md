# Image Analysis

This aims to detail the technical implementation of the image analysis and AI models included in Photonix.

As of the 2026 ML overhaul, every neural model runs on [ONNX Runtime](https://onnxruntime.ai/) rather than TensorFlow. This cut the installed image size by over a gigabyte, reduced per-classifier memory several-fold and sped up analysis by 1-2 orders of magnitude (details per model below). Before inference, large photos are downscaled so their longest edge is 1024 pixels (configurable via `CLASSIFIER_MAX_INFERENCE_SIZE`) — detection outputs are stored as relative coordinates so nothing downstream changes.


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
- [GeoNames cities1000](http://download.geonames.org/export/dump/) (Creative Commons Attribution 4.0 International License). This contains latitudes, longitudes and populations for all towns and cities in the world with a population over 1000.

Since 2026 the GeoNames data ships as `cities.bin` — a compact binary built offline by [`scripts/build_location_cities.py`](https://github.com/photonixapp/photonix/blob/master/scripts/build_location_cities.py) containing only the columns we use (name, coordinates, country code, population). This shrank the download from 22 MB to 4.3 MB (1.6 MB compressed) and the in-memory representation is numpy arrays, so the per-photo city lookup is fully vectorised. Outputs were verified identical to the old TSV path across a global grid sweep before the switch.

### Country

We first load the countries shapefile using the pure Python library [pyshp](https://github.com/GeospatialPython/pyshp). We then loop over each country and load it's polygon into [matplotlib's path module](https://matplotlib.org/3.1.0/api/path_api.html). We can then use a convenient function from the module `contains_points` to determine if our photo's location is within the country's border.

One notable point is that the country polygons are not particularly detailed. Currently it works well if the photo is taken inland but photos taken on beaches can sometimes miss out. A future enhancement would be to broaden the search radius (within reason) to try and get within the nearest country's border. A more detailed shapefile of countries could also be procured but the extra points could really slow things down.

### City

This is much simpler than the calculation for country. We calculate the distance between every city and our photo's coordinates in one vectorised numpy pass using the [`haversine`](https://en.wikipedia.org/wiki/Haversine_formula) formula. This is fairly simplistic as it assumes a spherical world and doesn't account for terrain but is good enough (and fast enough) for our use case. We exclude any cities that have a distance over 10km and return the nearest one (if any).


## Style Classification

A small MobileNet-based classifier retrained on a hand-curated dataset of photographic styles (macro, serene, etc.) — the training scripts live at [`photonix/classifiers/style/`](https://github.com/photonixapp/photonix/tree/master/photonix/classifiers/style). Images are resized to 224 × 224 and normalised before inference. The model was converted from its original TensorFlow frozen graph to ONNX (17 MB, fp32) with verified output parity; a tag is only applied when a style scores above 0.66.

## Object Recognition

We use an SSD MobileNet v2 detector trained on [Open Images V4](https://storage.googleapis.com/openimages/web/factsfigures_v4.html), which gives us a rich vocabulary of ~600 everyday labels ("Sunglasses", "Wine glass"…) plus bounding boxes, which the UI shows as hoverable regions on the photo.

Originally this ran as a TensorFlow frozen graph. During the ONNX migration we found the graph's embedded control-flow NMS (non-maximum suppression) made ONNX Runtime take about a minute to initialise the session, so the shipped model is a backbone-only conversion: the network outputs raw box encodings and class logits, and box decoding + NMS run as vectorised numpy in [`photonix/classifiers/object/model.py`](https://github.com/photonixapp/photonix/blob/master/photonix/classifiers/object/model.py). Detections are byte-identical to the original graph, the session now initialises in ~0.2 s, and a photo is analysed in ~0.1 s on a desktop CPU (vs several seconds before the migration).

## Face Detection and Recognition

The original pipeline was completed in June 2021 (MTCNN + FaceNet on TensorFlow) and was replaced in 2026 with InsightFace's SCRFD detector and ArcFace embeddings on ONNX Runtime — shrinking the download from 91 MB to 16 MB and cutting analysis time and memory by an order of magnitude. There are a few different steps to the process. Facial recognition is different from our other types of analysis as it only becomes useful if the user can label the people they know. Because of this, part of the model is automatically re-trained to apply the user's own face labels.

Papers With Code provides [benchmark comparisons of algorithms](https://paperswithcode.com/area/computer-vision/facial-recognition-and-modelling) for each step (and more).

### Face Detection

We use [SCRFD](https://arxiv.org/abs/2105.04714) (the 500M-FLOPs variant from the [InsightFace](https://github.com/deepinsight/insightface) project), a modern anchor-free face detector that runs as a 2.5 MB ONNX model. It substantially out-performs the MTCNN detector we used from 2021-2026 — particularly on small, rotated and partially occluded faces — while being over an order of magnitude faster. Images are letterboxed into a 640 × 640 input; the decoded boxes and five facial keypoints (eyes, nose, mouth corners) are mapped back to full-resolution pixel space.

The bounding box output of running this model against photos is used to create location-specific tags in the database. These tags are of unknown people at this stage but it's still useful to tag the information in the database at this step.

### Face Alignment / Transformation and Cropping

Because faces can be oriented and pointing in different directions we want to normalise them as much as possible. Using the five keypoints from the detector, a similarity transform (the [Umeyama algorithm](https://en.wikipedia.org/wiki/Kabsch_algorithm)) warps each face onto ArcFace's canonical 112 × 112 template so eyes, nose and mouth land in consistent positions.

### Feature Extraction / Embedding / Face Fingerprinting / Faceprinting

Aligned faces are embedded with a MobileFaceNet recognition network trained with the [ArcFace](https://arxiv.org/abs/1801.07698) loss on the WebFace600K dataset (the `w600k_mbf` model from InsightFace, 13.6 MB ONNX). It outputs a 512-dimensional embedding which we L2-normalise. You can think of the dimensions as features of the face, and together they make up a kind of fingerprint. This replaced the 128-dimensional FaceNet embeddings used previously — when upgrading, Photonix automatically re-analyses previously scanned faces (existing person names are preserved by matching bounding-box positions) via the housekeeping job.

The embedding of a face image only needs to be computed once and then it gets saved against the face tag in the database, ready for the next step.

### Similarity Calculation / Clustering / Classification

The face embeddings (or fingerprints) have been generated and saved but no two photos of the same face will match exactly. There are always slight variations caused by things like lighting, orientation, emotion and hair. We can however calculate how similar one embedding is to another using a distance formula. The recommended formula for FaceNet is the [Euclidean distance](https://en.wikipedia.org/wiki/Euclidean_distance) which can compare all 512 dimensions of our embedding and give us a single number as a result.

A threshold is decided upon and if the Euclidean distance of two face embeddings is below this value then we assume the photos to be of the same person.

Computing the distance between two embeddings is quite fast but as more and more photos of faces are added to your library the number of comparisons you would have to do between them increases exponentially. To solve this issue we implement an ANN (Approximate [Nearest Neighbors](https://en.wikipedia.org/wiki/Nearest_neighbor_search)) search index using the [Annoy](https://github.com/spotify/annoy) library. This is what Spotify uses to suggest similar songs you might like and it is able to do this for every user, every day across its entire library of tracks.

The ANN is fast to generate and is re-created at 5-minutely intervals if new face tags have been added since last generation. A hybrid approach is used whereby any face tags added since last index generation are compared individually. This means that similar face photos imported within a short period of time will still match (it just takes a bit longer until the index catches up).

### Labelling

An interesting point to note is that similar faces can be grouped together even if we don't know who the person is. Because of this, if a face photo isn't similar enough to a face labelled by the user we create a random tag name in the form "Unknown person 123456" where the number is random. Grouping happens while photos are imported and the user just has to go and change the tag name to the person they know.

We are slightly cautious while we are grouping faces together as it is much easier for a user to merge two groups that are actually the same rather than having to remove faces from a group.

Our user interface shows bounding boxes for faces and allows quick approval, rejection and editing of automatic face tags.


## Semantic Search (CLIP)

Added in 2026, this is the seventh analyzer and powers the "Natural language" search mode — you describe what you're looking for ("dog on a beach at sunset") and get photos ranked by how well they match. It is opt-in per library because the models are the largest download in the system (~340 MB).

We use OpenAI's [CLIP](https://openai.com/research/clip) ViT-B/32, which embeds images and text into the same 512-dimensional space. The image encoder runs int8-quantized (89 MB, verified to preserve retrieval quality) and embeds each photo once at import time (~20 ms per photo on a desktop CPU). The text encoder stays at full precision (254 MB) since it only runs once per search query — our testing showed quantizing it measurably degraded ranking quality. Text is tokenized with a vendored pure-Python implementation of CLIP's BPE tokenizer.

Photo embeddings are stored in the database and indexed per-library into an [Annoy](https://github.com/spotify/annoy) approximate-nearest-neighbour index (the same library the face recognition uses), refreshed every few minutes. A search encodes the query text, pulls the top matches from the index, brute-force-scans any embeddings newer than the index, and returns photos ordered by cosine similarity.

The CLIP weights are MIT-licensed (via [immich-app's ONNX exports](https://huggingface.co/immich-app/ViT-B-32__openai)).
