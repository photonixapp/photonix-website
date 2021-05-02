# Upgrading

## Docker Compose

Assuming you already have Photonix running using Docker Compose, this will let you upgrade to the latest version with minimum downtime. Pulling the new image may take several minutes, depending on your download speed.

```bash
docker-compose pull photonix
docker-compose stop photonix
docker-compose up -d photonix
```

## Automatic upgrades via Watchtower

[Watchtower](https://containrrr.dev/watchtower/) can be run as a service to keep Photonix (and your other Docker images) updated to the latest version.

It will regularly try and `docker pull` the images of your running services and restart them when necessary. Note that this could prevent Photonix from being acessible for short periods of time and interrupt things like uploads. There are config options for setting things like interval and schedules.

In most cases you can add it to  `docker-compose.yml` like so:

```yaml
services:
  watchtower:
    container_name: watchtower
    image: containrrr/watchtower
    restart: unless-stopped
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
    command: --interval 86400  # Check every 24 hours (in seconds)
```
