FROM python:3.10-slim

WORKDIR /azure-graph-api

ADD / /azure-graph-api

RUN apt-get update \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r ./requirements.txt

# EXPOSE 80

ENTRYPOINT ["python", "app.py"]