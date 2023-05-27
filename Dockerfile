FROM ubuntu:22.04

RUN apt-get update && apt-get install -y
RUN apt-get install -y curl
RUN apt-get install -y nginx
RUN apt-get install -y python3
RUN apt-get install -y postgresql-client
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs

RUN mkdir -p /redarc
WORKDIR /redarc
COPY . .

RUN mv config_default.json config.json
RUN npm ci

WORKDIR /redarc/redarc-frontend
RUN npm ci

WORKDIR /redarc
RUN chmod +x scripts/start.sh
CMD ["scripts/start.sh"]