# AI Models

This aims to detail the technical implementation of the image analysis models embedded in Photonix.

## Color Analysis

Details coming soon.

## Location Detection

Details coming soon.

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
