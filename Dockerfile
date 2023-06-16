FROM node:16-alpine3.17

RUN apk update
# Download the runtime dependencies
RUN apk add --no-cache bash nginx python3 postgresql-client

RUN mkdir -p /redarc
WORKDIR /redarc
COPY . .

RUN mv config_default.json config.json
RUN npm ci

WORKDIR /redarc/redarc-frontend
RUN npm ci

WORKDIR /redarc
RUN chmod +x scripts/start.sh
CMD ["/bin/bash", "scripts/start.sh"]