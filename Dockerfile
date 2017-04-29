FROM debian:jessie

RUN apt-get update && \
    apt-get install -y nginx-light=1.6.2-5+deb8u4 && \
        apt-get clean && \
            rm -rf /var/lib/apt/lists/* \
                   /tmp/* \
                   /var/tmp/*

COPY public /srv
COPY nginx.conf /etc/nginx/nginx.conf

WORKDIR /srv
CMD nginx

EXPOSE 80
