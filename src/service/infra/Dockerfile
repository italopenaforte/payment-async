FROM python:3.11.4-slim

WORKDIR /srv/app

COPY . .

RUN apt-get update && \
    apt-get autoremove && \
    apt-get autoclean && \
    pip install --no-cache-dir -r /srv/app/requirements.txt && \
    python -m compileall -f /srv/app/

CMD ["uvicorn src.service.main:app --reload"]
