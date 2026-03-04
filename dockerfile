FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./ 

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .

COPY app/ ./app/

EXPOSE 8000
