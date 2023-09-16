FROM alpine3.18

RUN apk update

RUN apk add bash python3 py3-pip postgresql-client

RUN mkdir -p /index_worker
WORKDIR /index_worker
COPY . .

RUN pip install python-dotenv
RUN pip install psycopg2-binary

CMD ["/bin/python3", "index_worker.py"]