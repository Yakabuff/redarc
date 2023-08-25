FROM node:16-alpine3.17

RUN apk update
# Download the runtime dependencies
RUN apk add --no-cache bash nginx python3 postgresql-client

RUN mkdir -p /redarc
WORKDIR /redarc
COPY . .

RUN mv /redarc/api/config_default.json /redarc/api/config.json
WORKDIR /redarc/api
RUN npm ci

WORKDIR /redarc/frontend
RUN npm ci

WORKDIR /redarc
RUN chmod +x scripts/start.sh
CMD ["/bin/bash", "scripts/start.sh"]