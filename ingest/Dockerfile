FROM redis:7.0.12-alpine3.18

RUN apk update

RUN apk add bash python3 py3-pip postgresql-client

RUN mkdir -p /ingest
WORKDIR /ingest
COPY . .

RUN pip install rq
RUN pip install python-dotenv
RUN pip install praw
RUN pip install psycopg2-binary
RUN pip install gallery-dl

RUN chmod +x entry.sh
CMD ["/bin/bash", "entry.sh"]