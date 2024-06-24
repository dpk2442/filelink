# Python build container
FROM python:3.12-slim as python-build
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && \
    apt-get -y install build-essential mime-support libpcre3 libpcre3-dev && \
    pip install --upgrade pip && \
    pip install virtualenv && \
    virtualenv .venv && \
    ./.venv/bin/pip install -r requirements.txt

# Final container
FROM python:3.12-slim
WORKDIR /app

RUN apt-get update && \
    apt-get -y install libpcre3

# Install mime support
COPY --from=python-build /etc/mime.types /etc/mime.types

# Expose ports
EXPOSE 9090

# Copy local files
COPY . .

# Copy virtual env
COPY --from=python-build /app/.venv ./.venv

# Run start script
CMD ["./run.sh"]
