FROM alpine:3.18

RUN apk update

RUN apk add bash python3 py3-pip postgresql-client

RUN mkdir -p /reddit_worker
WORKDIR /reddit_worker
COPY . .

RUN pip install rq
RUN pip install python-dotenv
RUN pip install praw
RUN pip install psycopg2-binary

CMD ["python3", "reddit_worker.py"]