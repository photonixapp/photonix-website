# Credits and Licenses

Photonix wouldn't be possible without being able to stand on the shoulders of giants that make the libraries we use. Here we try to list all the main ones and the open source licenses that they are released under.

## Backend Server Side

- [Django](https://www.djangoproject.com/) ([BSD 3-clause License](https://github.com/django/django/blob/main/LICENSE)) Python web framework
- [PostgreSQL](https://www.postgresql.org/) ([PostgreSQL License](https://www.opensource.org/licenses/postgresql)) Relational database management system
- [Redis](https://redis.io/) ([BSD 3-clause License](https://github.com/redis/redis/blob/unstable/COPYING)) In-memory data structure store
- [Graphene](https://graphene-python.org/) ([MIT License](https://github.com/graphql-python/graphene/blob/master/LICENSE)) GraphQL library
- [Django GraphQL JWT](https://django-graphql-jwt.domake.io/en/latest/) ([MIT License](https://github.com/flavors/django-graphql-jwt/blob/master/LICENSE)) Django authentication using GraphQL and JWT
- [PyJWT](https://pyjwt.readthedocs.io/en/latest/) ([MIT License](https://github.com/jpadilla/pyjwt/blob/master/LICENSE)) JSON Web Token library
- [Requests](https://docs.python-requests.org/en/master/index.html) ([Apache-2.0 License](https://github.com/psf/requests/blob/master/LICENSE)) HTTP library
- [Pytz](https://pythonhosted.org/pytz/) (MIT License) Timezone supprt library
- [asyncinotify](https://asyncinotify.readthedocs.io/en/latest/) ([MIT License](https://gitlab.com/Taywee/asyncinotify/-/blob/master/LICENSE)) inotify file watching library based on Asyncio
- [Pillow](https://python-pillow.org/) ([HPND License](https://github.com/python-pillow/Pillow/blob/master/LICENSE)) Image manipulation library

## Image Analysis

More details on the useage of these can be found on the [Image Analysis](https://photonix.org/docs/developer/image_analysis/) page.

- [Tensorflow](https://www.tensorflow.org/) ([Apache-2.0 License](https://github.com/tensorflow/tensorflow/blob/master/LICENSE)) Machine learning framework
- [Keras](https://keras.io/) ([Apache-2.0 License](https://github.com/keras-team/keras/blob/master/LICENSE)) Deep learning framework
- [Numpy](https://numpy.org/) ([BSD 3-clause License](https://github.com/numpy/numpy/blob/main/LICENSE.txt)) High performance data processing library
- [SciPy](https://www.scipy.org/) ([BSD 3-clause License](https://github.com/scipy/scipy/blob/master/LICENSE.txt)) Mathematics, science, and engineering library

### Color Detection

- [Pillow](https://python-pillow.org/) ([HPND License](https://github.com/python-pillow/Pillow/blob/master/LICENSE)) Image manipulation library
- [Numpy](https://numpy.org/) ([BSD 3-clause License](https://github.com/numpy/numpy/blob/main/LICENSE.txt)) High performance data processing library

### Location Detection

- [PyShp](https://github.com/GeospatialPython/pyshp) ([MIT License](https://github.com/GeospatialPython/pyshp/blob/master/LICENSE.TXT)) ESRI Shapefile library
- [Matplotlib](https://matplotlib.org/) ([License](https://github.com/matplotlib/matplotlib/blob/master/LICENSE/LICENSE)) Visualization library
- [World Borders Dataset](http://thematicmapping.org/downloads/world_borders.php) ([Creative Commons Attribution-Share Alike 3.0 License](http://creativecommons.org/licenses/by-sa/3.0/)) Shapefile polygons of contries of the world
- [GeoNames Top 1000 Cities](http://download.geonames.org/export/dump/) ([Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/)) City locations and populations

### Style Classification

Based on the paper [Recognizing Image Style [2013]](https://arxiv.org/abs/1311.3715) by Sergey Karayev et al.

- [Tensorflow](https://www.tensorflow.org/) ([Apache-2.0 License](https://github.com/tensorflow/tensorflow/blob/master/LICENSE)) Machine learning framework
- [MobileNet](https://opensource.googleblog.com/2017/06/mobilenets-open-source-models-for.html) Deep neural network architecture
- [Flickr](https://www.flickr.com/) Used as labelled dataset of styles

### Object Detection

- [MobileNet](https://opensource.googleblog.com/2017/06/mobilenets-open-source-models-for.html) Deep neural network architecture

### Face Detection and Recognition

Based on the papers [Joint Face Detection and Alignment using Multi-task Cascaded Convolutional Networks [2016]](https://arxiv.org/abs/1604.02878) by Kaipeng Zhang et al. and [FaceNet: A Unified Embedding for Face Recognition and Clustering[2015]](https://arxiv.org/abs/1503.03832) by Florian Schroff et al.

- [MTCNN implementation](https://github.com/ipazc/mtcnn) ([MIT License](https://github.com/ipazc/mtcnn/blob/master/LICENSE)) Face detection convolutional neural network based on Keras/Tensorflow
- [Deepface](https://github.com/serengil/deepface) ([MIT License](https://github.com/serengil/deepface/blob/master/LICENSE)) Implementation of FaceNet (and other networks) for embeddings, utilities for transformation and distance metrics
- [Annoy](https://github.com/spotify/annoy) ([Apache-2.0 License](https://github.com/spotify/annoy/blob/master/LICENSE)) Highly performant Approximate Nearest Neighbors library for search
- [Tensorflow](https://www.tensorflow.org/) ([Apache-2.0 License](https://github.com/tensorflow/tensorflow/blob/master/LICENSE)) Machine learning framework
- [Keras](https://keras.io/) ([Apache-2.0 License](https://github.com/keras-team/keras/blob/master/LICENSE)) Deep learning framework

## Frontend User Interface (UI)

- [React](https://reactjs.org/) ([MIT License](https://github.com/facebook/react/blob/master/LICENSE)) Declarative, efficient, and flexible JavaScript library for building user interfaces
- [Redux](https://redux.js.org/) ([MIT License](https://github.com/reduxjs/redux/blob/master/LICENSE.md)) State container library for JavaScript apps
- [Apollo Client](https://www.apollographql.com/) ([MIT License](https://github.com/apollographql/apollo-client/blob/main/LICENSE)) GraphQL JS client library
- [Chakra](https://chakra-ui.com/) ([MIT License](https://github.com/chakra-ui/chakra-ui/blob/main/LICENSE)) UI component library
- [Babel](https://babeljs.io/) ([MIT License](https://github.com/babel/babel/blob/main/LICENSE)) JavaScript transpiler
- [Webpack](https://webpack.js.org/) ([MIT License](https://github.com/webpack/webpack/blob/master/LICENSE)) Code and asset bundler
- [React Swipeable](https://formidablelabs.github.io/react-swipeable/) ([MIT License](https://github.com/FormidableLabs/react-swipeable/blob/main/LICENSE)) Swipe gesture event handler hook

### Map View

- [Leaflet](https://leafletjs.com/) ([License](https://github.com/Leaflet/Leaflet/blob/master/LICENSE)) Library for interactive maps
- [Leaflet.markercluster](https://github.com/Leaflet/Leaflet.markercluster) ([MIT License](https://github.com/Leaflet/Leaflet.markercluster/blob/master/MIT-LICENCE.txt)) Animated map marker clustering library

## Packaging

- [Docker](https://www.docker.com/) ([Apache License 2.0](https://github.com/docker/docker-ce/blob/master/LICENSE)) Container build tools
- [PyPI](https://pypi.org/) Python Package Index
- [Pip](https://pip.pypa.io/en/stable/) ([MIT License](https://github.com/pypa/pip/blob/main/LICENSE.txt)) Python package installer
- [NPM](https://www.npmjs.com/) Node JS package manager registry
- [Yarn](https://yarnpkg.com/) ([BSD-2-Clause License](https://github.com/yarnpkg/berry/blob/master/LICENSE.md)) JS package manager

## Testing

- [Pytest](https://docs.pytest.org/en/latest/) ([MIT License](https://github.com/pytest-dev/pytest/blob/main/LICENSE)) Python testing framework
- [Factory Boy](https://factoryboy.readthedocs.io/en/stable/) ([MIT License](https://github.com/FactoryBoy/factory_boy/blob/master/LICENSE)) Python test fixtures replacement
- [Coverage](https://coverage.readthedocs.io/en/coverage-5.5/) ([Apache-2.0 License](https://github.com/nedbat/coveragepy/blob/master/LICENSE.txt)) Python test coverage measurement
