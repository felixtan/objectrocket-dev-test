FROM ubuntu:18.10
LABEL maintainer='contact@felixtan.io'

RUN apt-get update && \
    apt-get install -y python3

COPY . /home

ENTRYPOINT ["./home/checkout.py"]