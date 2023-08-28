FROM node:16-alpine3.17

RUN apk update
# Download the runtime dependencies
RUN apk add --no-cache bash nginx python3 py3-pip postgresql-client

RUN mkdir -p /redarc
WORKDIR /redarc
COPY . .

RUN pip install gunicorn
RUN pip install falcon
RUN pip install rq
RUN pip install python-dotenv
RUN pip install psycopg2-binary

WORKDIR /redarc/frontend
RUN npm ci

WORKDIR /redarc
RUN chmod +x scripts/start.sh
CMD ["/bin/bash", "scripts/start.sh"]