# Installing and Running

The easiest way to run it is with [Docker Compose](https://docs.docker.com/compose/install/#install-compose) using the pre-built image following these steps.

## Installing Docker and Docker Compose

You'll first need to install Docker and Docker Compose if you don't already have them.

- [Docker installation instructions](https://docs.docker.com/get-docker/)
- [Docker Compose installation instructions](https://docs.docker.com/compose/install/)

Installing these on recent versions of Debian, Ubuntu or Raspberry Pi OS can be done with the following commands and then logging out and back in.

    sudo apt update
    sudo apt install docker.io docker-compose
    sudo usermod -aG docker $USER

If `usermod` is not available on your system then you can do it the manual way and edit `/etc/group` adding your username to end of the line that starts with `docker:`.

Finally check Docker is running and you have the right permissions by running the following. You should see some table headings beginning with `CONTAINER ID` but you won't have any actual containers running yet.

    docker ps

If you still don't have permission, you may need to restart the whole machine.

## Setting up

Create a new directory to run inside.

    mkdir photonix
    cd photonix

Download the example Docker Compose file. This works for x86/amd64 and arm32/arm64/Raspberry Pi architectures.

    curl https://raw.githubusercontent.com/photonixapp/photonix/master/docker/docker-compose.example.yml > docker-compose.yml

Make volume directory for photo data to be stored outside the container.

    mkdir -p data/photos

## Running

Bring up Docker Compose which will pull and run the required Docker images.

    docker-compose up -d

The above command will run the service in the background. Instead, if you want to watch the logs (useful for debugging problems) you can use the following.

    docker-compose up

A few seconds after starting you should be able to go to [http://localhost:8888/](http://localhost:8888/) in your browser.

When you first access Photonix it will guide you through the process of creating an admin user, password and your first library.

You can move some photos into the folder `data/photos` and they should get detected and imported immediately. Once you have finished trying out the system you can edit the volume in the `docker-compose.yml` file where it says `./data/photos` to mount wherever you usually keep photos. System database, thumbnails and other cache data is stored separately from the photos so shouldn't pollute the area. You are responsible for keeping your own backups in case of error.

You can add extra users and libraries but this needs to be done on the command-line right now so run this in a new terminal window. Replace `USERNAME` with your own username.

    docker-compose run photonix python photonix/manage.py createsuperuser --username USERNAME --email example@example.com
    docker-compose run photonix python photonix/manage.py create_library USERNAME "My Library"


## Running image analysis in a separate container (optional)

By default the main `photonix` container does everything, including image analysis. If analysis is competing with serving your photos — or you'd like it to run on a beefier machine — you can move all of it into the dedicated `photonixapp/photonix-ml` image, built from the same codebase.

In your `docker-compose.yml`:

1. Add `CLASSIFICATION_DISABLED: 1` to the main `photonix` service's `environment` section. It will then run no analysis workers at all.
2. Add a `photonix-ml` service using the `photonixapp/photonix-ml:latest` image, with the same Postgres/Redis environment variables and the same `/data` volume mounts as the main service. The example compose file contains a ready-made commented-out block for this.

The ML container processes the shared analysis queue directly, so it needs network access to the same Postgres and Redis and a shared mount of the photo and model volumes (e.g. over NFS if it runs on a different machine). It waits for the main container to apply database migrations before starting, so start-up order doesn't matter.

Semantic search queries are still answered by the main container (encoding your search text is lightweight); only the per-photo analysis moves to the sidecar.
