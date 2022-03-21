FROM ubuntu:latest

RUN apt-get update \
    && apt-get install software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install -y git
RUN apt-get install -y python3.7-dev \
    && apt-get install python3.7 python3-pip \
    && apt-get install mysql-client \
    && apt-get install unixodbc-dev

RUN pip install -r requirements.txt

COPY . /Python-Programming/ixn-team-9
WORKDIR /Python-Programming/ixn-team-9
