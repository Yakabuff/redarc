FROM alpine3.18

RUN apk update

RUN apk add bash python3 py3-pip

RUN mkdir -p /image_downloader
WORKDIR /image_downloader
COPY . .

RUN pip install rq
RUN pip install python-dotenv
RUN pip install gallery-dl

CMD ["/bin/python3", "image_downloader.py"]