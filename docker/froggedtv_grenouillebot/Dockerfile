FROM debian

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN apt-get update && apt-get -y upgrade
RUN apt-get -y install python3-pip

RUN pip3 install \
    irc

ENV PYTHONPATH $PYTHONPATH:/froggedtv_grenouillebot

COPY . /froggedtv_grenouillebot/
