FROM alpine3.18

RUN apk update

RUN apk add bash python3 py3-pip

RUN mkdir -p /subreddit_worker
WORKDIR /subreddit_worker
COPY . .

RUN pip install rq
RUN pip install python-dotenv
RUN pip install praw

RUN chmod +x entry.sh
CMD ["/bin/python3", "subreddit_worker"]