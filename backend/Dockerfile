FROM python:3.13-slim

# build dependencies for psycopg2 (built from source) and other native packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt requirements-dev.txt /app/
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
