FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    gcc \
    python3-dev \
    libc-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG DB_URL
ARG BUILD_PATH
ARG REPO_PATH
ARG VERSION_POLL_TIME

EXPOSE 5000

CMD ["flask", "run"]