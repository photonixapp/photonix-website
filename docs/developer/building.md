# Building for Production

Photonix supports multiple architectures (amd64, arm32v7, arm64v8). We use Docker to build the server-side app image which provides a consistent runtime and can be run on Linux, Windows or MacOS. Building an amd64 image on a amd64 machine is simple enough and can be done with the standard Docker installation. For other architectures, we cross-compile using an experimental Docker extension called buildx.


## Automated builds

Docker images for all supported architectures get built automatically via GitHub Actions and Docker buildx. New releases can be created by tagging the latest commit on the `master` branch and this will trigger a new build.

    git tag v1.0.0
    git push --tags

Pushed images end up on [our Docker Hub page](https://hub.docker.com/repository/docker/photonixapp/photonix/tags) tagged as `latest` and parts of the version number - in this example, `1.0.0`, `1.0` and `1`. You can view existing tags from the repo to determine the next version with `git tag`.

More details about the buildx process can be read further down in the [Cross-compiled Docker Images](#cross-compiled-docker-images).


## Native Architecture Docker Image

From the cloned respository you should be able to run the following to build for the current architecture:

    make build-prd

To run the production image run the following:

    make start-prd


## Cross-compiled Docker Images

If you want to compile for an architecture different to what you are running (e.g. compiling for ARM on an x86 machine), you'll need to have the *Docker buildx* extension installed and bootstrapped for cross-compilation. The following are simplified instructions but you can find the [source material here](https://jite.eu/2019/10/3/multi-arch-docker/).


### Setting up Docker buildx

First we turn on experimental features in Docker daemon. Edit the file `/etc/docker/daemon.json` and add the following.

    {
      "experimental": true
    }

Restart the server.

    service docker restart

Now we enable experimental features in the client. Edit `~/.docker/config.json` and add this inside the top-level object:

    "experimental": "enabled"

We then need to download and install the buildx plugin. You may want to pick a newer version but this is the latest at time of writing.

    mkdir -p ~/.docker/cli-plugins/
    curl -L  https://github.com/docker/buildx/releases/download/v0.5.1/buildx-v0.5.1.linux-amd64 -o ~/.docker/cli-plugins/docker-buildx
    chmod +x ~/.docker/cli-plugins/docker-buildx

Run this to check whether the plugin is installed correctly:

    docker help | grep buildx

You should expect to see something like this:

    buildx*     Build with BuildKit (Docker Inc., v0.5.1)

You'll need to create a builder container for buildx:

    docker buildx create --name my-new-builder --driver docker-container --use

At this point buildx will only support your current architecture. To bootstrap support for all architectures run this:

    docker buildx inspect --bootstrap

You should see a list of supported platforms at the end of the above command.

### Building Docker images

You can then start building for your desired architecture, setting `--platform` in the command below to your desired architecture. Currently `linux/amd64`, `linux/arm64` and `linux/arm/v7` are supported.

    docker buildx build --platform linux/amd64,linux/arm/v7,linux/arm64 --tag photonixapp/photonix --push -f docker/Dockerfile.prd .

Buildx uses a different storage backed to standard Docker so build images will not display when running the `docker images` command and cannot be easily run. For this reason it is recommended to be logged in with `docker login` and push at the same time (`--push` in the shown command). You can change the tag to upload to your personal Docker Hub account by changing `--tag YOUR_USERNAME/photonix` in the command above.

### Upgrading and caching Python packages

For users upgrading Python dependencies, some packages with C extensions (e.g. Numpy and Matplotlib) will need compiling for ARM architectures which takes a long time. These packages can be automatically uploaded to our custom PyPI server to speed up future builds. You'll need write access to the PyPI server and specify authentication credentials with `--build-ags` as shown below.

    docker buildx build --platform linux/amd64,linux/arm/v7,linux/arm64 --tag photonixapp/photonix --pusbehave differentlyh -f docker/Dockerfile.prd --build-arg PYPI_UPLOAD_USERNAME=YOUR_USERNAME --build-arg PYPI_UPLOAD_PASSWORD=YOUR_PASSWORD .

### Potential errors

It might be due to the fact that buildx is experimental or that some base images differ between architectures but we found several inconsistencies. Builds would fail at a certain point on one architecture but be fine in another. Building directly on a Raspberry Pi would work successfully when cross-compiling for it wouldn't (even when using buildx on the Pi).

It can be a very fiddly job to get all architectures working - getting buildx working for all architectures initially took solid weeks of work spread across many months.

You may need so switch some commands for slightly different ones install extra packages. It can also be useful to break down multi-line docker `RUN` commands to find errors and speed up iterations. It's also good to have a real device (like a Raspberry Pi) SSH'd into to confirm running the same command there produces the same error.
