FROM python:3.11.4-slim

WORKDIR /srv/app

COPY . /srv/app

RUN apt-get update && \
    apt-get autoremove && \
    apt-get autoclean && \
    pip install --no-cache-dir -r /srv/app/requirements.txt && \
    python -m compileall -f /srv/app/

CMD ["/srv/app/entrypoint.sh"]
