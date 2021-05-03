# Developer documentation

## Getting started

There is a [`Makefile`](./Makefile) and separate Docker Compose file `docker-compose.dev.yml` that you should use if you want to work on the project. Check out the repo and this setup will build the image, mount the code as volumes, hot-reload JS changes to the browser and reload the Python server for most changes.

    git clone git@github.com:photonixapp/photonix.git
    cd photonix
    mkdir -p  data/photos
    make build
    make start

You should now be able to access the app in your browser at [http://localhost:8888/](http://localhost:8888/).

If you want to access the Bash or Python shells for development, you can use the following command.

    make shell


## Common Problems

### Port Number Clashes

If you get errors such as `Error starting userland proxy: listen tcp 0.0.0.0:5432: bind: address alerady in use` then you probably have an existing server such as Postgres listening on the standard port. You can change Photonix's services to use alternative port numbers by editing `docker/docker-compose.dev.yml` and setting `'5432:5432'` to be `'5433:5432'` for example. This is for Postgres but is it a similar solution for Redis or the webserver ports.
