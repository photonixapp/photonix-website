# Reverse Proxies

Using a reverse proxy allows you to host Photonix and other services in a more professional way.

Benefits:
- Users can access services without specifying a port number in the URL.
- Each service can have it's own hostname or subdomain.
- HTTPS/SSL can be enabled with certificates. Many solutions like Traefik will integrate with [LetsEncrypt](https://letsencrypt.org/) to auto-generate and renew certificates.

## Traefik

This example shows Traefik running in front of Photonix on a custom domain with HTTPS enabled and certificate renewing using [LetsEncrypt](https://letsencrypt.org/).

If you use this, make sure you change `email@example.com` to your own email address for LetsEncrypt certificate error notification, `photonix.example.com` to your own domain name and make sure the volumes map point to valid paths.

Note: It is easy to get blocked from LetsEncrypt for a period of time if you make too many invalid requests. Therefore it's recommended to use their staging server to get your first certificate.

See the [Traefik docs](https://doc.traefik.io/traefik/) for more information.

```
services:
  traefik:
    image: "traefik:v2.2"
    restart: always
    container_name: "traefik"
    command:
      - "--log.level=DEBUG"
      - "--api.insecure=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.web.http.redirections.entryPoint.to=websecure"
      - "--entrypoints.web.http.redirections.entryPoint.scheme=https"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.myresolver.acme.tlschallenge=true"
#      - "--certificatesresolvers.myresolver.acme.caserver=https://acme-staging-v02.api.letsencrypt.org/directory"  # Useful for testing certificate generation
      - "--certificatesresolvers.myresolver.acme.email=email@example.com"
      - "--certificatesresolvers.myresolver.acme.storage=/letsencrypt/acme.json"
    ports:
      - "80:80"
      - "443:443"
      - "8080:8080"
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock:ro"
      - "/volumes/letsencrypt:/letsencrypt"

  photonix:
    container_name: photonix
    image: damianmoore/photonix:latest
    restart: always
    ports:
      - '8888:80'
    environment:
      ENV: prd
      POSTGRES_HOST: postgres
      POSTGRES_DB: photonix
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      REDIS_HOST: redis
      ALLOWED_HOSTS: '*'
    volumes:
      - /volumes/photonix/photos:/data/photos
      - /volumes/photonix/raw-photos-processed:/data/raw-photos-processed
      - /volumes/photonix/cache:/data/cache
      - /volumes/photonix/models:/data/models
    links:
      - postgres
      - redis
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.photonix.rule=Host(`photonix.example.com`)"
      - "traefik.http.routers.photonix.entrypoints=websecure"
      - "traefik.http.routers.photonix.tls.certresolver=myresolver"
      - "traefik.http.services.photonix.loadbalancer.server.port=80"
```
