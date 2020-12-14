FROM python:3.6.8-slim-stretch

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        libpq-dev \
        nginx-light \
        python3-dev \
        supervisor \
        && \
        apt-get clean && \
            rm -rf /var/lib/apt/lists/* \
                   /tmp/* \
                   /var/tmp/*

WORKDIR /srv
COPY requirements.txt /srv/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY blog /srv/blog
COPY docs /srv/docs
COPY mailinglist /srv/mailinglist
COPY static /srv/static
COPY project /srv/project
COPY system /srv/system
COPY templates /srv/templates
COPY utils /srv/utils
COPY manage.py /srv/manage.py
COPY mkdocs.yml /srv/mkdocs.yml
COPY .git /srv/.git

ENV PYTHONPATH /srv

RUN python manage.py collectstatic --noinput --link
RUN mkdocs build -d /srv/docs_built

CMD ./system/run.sh

EXPOSE 80
