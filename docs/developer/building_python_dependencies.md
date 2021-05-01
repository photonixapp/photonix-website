# Building Python Dependencies

You shouldn't need to worry about this if you are just building production images but we like to have the steps documented in case we need to upgrade dependencies in future.

Several Python packages are compiled (C extensions etc.) for performance reasons. Usually this in transparent to a developer installing via something like *pip* but there are a couple of packages where we had to put more effort in to building. The Python packages we build are uploaded to our [own PyPI server](https://pypi.epixstudios.co.uk/) and this gets searched when the main Docker images are built. There are often binary wheel packages missing from the [Official Python PyPI server](https://pypi.org/) especially for the ARM architectures so our PyPI server acts as a cache to speed up the main Docker builds.


## Building Tensorflow

Tensorflow is the Machine Learning library we use for our more complex image analysis features. It allows us to create algorithms to do things like detecting and recognising objects in a photo or identifying a style.

For maximum compatibility we compile our own builds of Tensorflow separately using the repository [tensorflow-builder](https://github.com/damianmoore/tensorflow-builder/). On the amd64 architecture we found the official binaries are built with a set of CPU instructions (e.g. AVX) aimed at recent CPUs which do not run on many home servers (e.g. Celeron CPUs). On the ARM platform there are a few official builds aimed at the Raspberry Pi but they are compiled against older versions of Python than we use.

Beware that building will probably take many hours but scales well to multiple CPUs. We usually create the largest possible VPS on DigitalOcean with 32 CPU cores and it can build each architecture in about an hour (per architecture).

These are the commands used to build on a fresh machine (Ubuntu 20.04).

```bash
# Set up Docker if not pre-installed
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Clone Tensorflow Builder repo
git clone https://github.com/damianmoore/tensorflow-builder.git
cd tensorflow-builder

# Build for one or all of the following architectures
./build.sh amd64
./build.sh arm32v7
./build.sh arm64v8
```

## Potential errors

You shouldn't run into these errors if you are just trying to build. However, if you are trying to upgrade dependencies at a later date this could help identify the problem.

### h5py expecting different version of Numpy

```bash
>>> import h5py
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/lib/python3.8/site-packages/h5py/__init__.py", line 46, in <module>
    from ._conv import register_converters as _register_converters
  File "h5py/_conv.pyx", line 1, in init h5py._conv
  File "h5py/h5t.pyx", line 1, in init h5py.h5t
ValueError: numpy.ndarray size changed, may indicate binary incompatibility. Expected 88 from C header, got 80 from PyObject
```

When h5py was compiled, it probably used whatever version of Numpy was the latest version. The [`install_and_upload_python_packages.py`](https://github.com/photonixapp/photonix/blob/master/docker/install_and_upload_python_packages.py) script works around this by `pip install`ing requirements one at a time with Numpy before Tensorflow (which is what includes h5py as a dependency). If you are using the custom PyPI server (which is the default behaviour for Photonix) then the previously built h5py wheel can be removed to force it to be rebuilt.

### Matplotlib/Tensorflow expecting different version of Numpy

```bash
>>> import matplotlib
RuntimeError: module compiled against API version 0xa but this version of numpy is 0x9
ImportError: matplotlib failed to import
```

This is similar to the h5py error above - when Matplotlib or Tensorflow got compiled, the wrong version of Numpy was installed. The [`install_and_upload_python_packages.py`](https://github.com/photonixapp/photonix/blob/master/docker/install_and_upload_python_packages.py) script works around this by `pip install`ing requirements one at a time with Numpy before matplotlib.

In the case of Tensorflow, the package is complex to compile so is built using [this repo](https://github.com/photonixapp/tensorflow-builder). It should all be handled via our [build script](https://github.com/photonixapp/tensorflow-builder/blob/master/build.sh) now as long as `NUMPY_VERSION` is set to the one recommended for the version of Tensorflow. Our script fixes the main Tensorflow repo by pinning Numpy to the correct version.


### Randomly stopping while building Tensorflow

Quite often building Tensorflow can fail without very helpful errors. I suggest taking note of where the build got to (e.g. `[15,686 / 23,361]`) and then starting the build again. If it fails again at a very different number (non-deterministic) then it might just be that it is running out of memory (OOM). We find the best way to build Tensorflow is by using a large VPS (see above).
