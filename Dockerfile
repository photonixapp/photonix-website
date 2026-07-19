FROM python:3.13-slim-trixie

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        libcairo2-dev \
        libpq-dev \
        nginx-light \
        pkg-config \
        python3-dev \
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
COPY docs-theme /srv/docs-theme
COPY mailinglist /srv/mailinglist
COPY static /srv/static
COPY project /srv/project
COPY system /srv/system
COPY templates /srv/templates
COPY testimonials /srv/testimonials
COPY utils /srv/utils
COPY manage.py /srv/manage.py
COPY mkdocs.yml /srv/mkdocs.yml
COPY .git /srv/.git
COPY faqs /srv/faqs
# COPY sponsors /srv/sponsors

ENV PYTHONPATH /srv

RUN python manage.py collectstatic --noinput --link
RUN mkdocs build -d /srv/docs_built

CMD ./system/run.sh

EXPOSE 80
