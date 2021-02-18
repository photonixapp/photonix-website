# Building for Production

Photonix supports (almost) multiple architectures (amd64, arm32v7, arm64v8). We use Docker to build the server-side app image which provides a consistent runtime and can be run on Linux, Windows or MacOS. Building an amd64 image on a amd64 machine is simple enough and can be done with the standard Docker installation. For other architectures, we cross-compile using an experimental Docker extension called buildx.


## Native Architecture Docker Image

From the checked-out respository you should be able to run the following to build:

    make build-prd

To run the production image run the following:

    make start-prd

## Cross-compiled Docker Images

You'll need to have the Docker buildx extension installed and bootstrapped for cross-compilation. The following are simplified instructions but you can find the [source material here](https://jite.eu/2019/10/3/multi-arch-docker/).

First we turn on experimental features in Docker daemon. Edit the file `/etc/docker/daemon.json` and add the following.

    {
      "experimental": true
    }

Restart the server

    service docker restart

Now we enable experimental features in the client. Edit `~/.docker/config.json` and add this:

    {
      "experimental": "enabled"
    }

We then need to download and install the buildx plugin. You may want to pick a newer version but this is the latest at time of writing.

    curl -L  https://github.com/docker/buildx/releases/download/v0.5.1/buildx-v0.5.1.linux-amd64 -o ~/.docker/cli-plugins/docker-buildx
    chmod +x ~/.docker/cli-plugins/docker-buildx

Run this to check whether the plugin is installed correctly

    docker help | grep buildx

You should expect to see something like this:

    buildx*     Build with BuildKit (Docker Inc., v0.5.1)

You'll need to create a builder container for buildx.

    docker buildx create --name my-new-builder --driver docker-container --use

At this point buildx will only support your current architecture. To boostrap support for all architectures run this:

    docker buildx inspect --bootstrap

You should see a list of supported platforms at the end of the above command.


## Building Tensorflow

Tensorflow is the Machine Learning library we use for our more complex image analysis features. It allows us to create algorithms to do things like detecting and recognising objects in a photo or identifying a style.

For maximum compatibility we compile our own builds of Tensorflow separately using the repository [tensorflow-builder](https://github.com/damianmoore/tensorflow-builder/). On the amd64 architecture we found the official binaries are built with a set of CPU instructions (e.g. AVX) aimed at recent CPUs which do not run on many home servers (e.g. Celeron CPUs). On the ARM platform there are a few official builds aimed at the Raspberry Pi but they are compiled against an older version of Python and Numpy than we use.

- Python integration
- Pre-built packages
- Device compatibility
- Build tools - Bazel, Docker
- Raspberry Pi
- Common problems
  - Pip package versions
  - OOM
    - Progress shown (e.g. [15,686 / 23,361]) - if you run again and it fails at a different stage then it's probably OOM

```
Execution platform: @local_execution_config_platform//:platform
In file included from /usr/include/python2.7/Python.h:8:0,
                 from ./tensorflow/python/lib/core/numpy.h:35,
                 from tensorflow/python/lib/core/numpy.cc:20:
/usr/include/python2.7/pyconfig.h:24:54: fatal error: arm-linux-gnueabihf/python2.7/pyconfig.h: No such file or directory
 #  include <arm-linux-gnueabihf/python2.7/pyconfig.h>
 ```
