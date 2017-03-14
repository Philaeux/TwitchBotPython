FROM debian

# Environment
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PYTHONPATH $PYTHONPATH:/grenouillebot

# Packages
RUN apt-get update && apt-get -y upgrade
RUN apt-get -y install python3-pip
RUN pip3 install \
    irc==15.0.6 \
    google-api-python-client==1.5.5

# Add code
COPY . /grenouillebot/
