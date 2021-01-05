# Photonix Website

Photonix website located at [photonix.org](https://photonix.org).


## Running

The following commands from the [Makefile](Makefile) can be used to build and run the server. This will start the main container and a Postgres database server.

```
make build
make start
```

If you need to change any environment variables you can do so in [docker-compose.yml](docker-compose.yml).


## Documentation

MkDocs is used to generate documentation from Markdown files in the [docs](docs) directory. If you run the with the envirnment variable `ENV=dev` as is default in [docker-compose.yml](docker-compose.yml) then the live-reloading server should be available at [http://localhost:8001](http://localhost:8001) for easily making changes. Just edit files ending in `.md` and you should see them update in the browser. For convenience here's a [Markdown Cheatsheet](https://www.markdownguide.org/cheat-sheet).
