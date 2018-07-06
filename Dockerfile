#############################
# Dockerfile for Meditech Bot
#############################

# Base on Ubuntu 16.04
FROM ubuntu:16.04

MAINTAINER Meditech Bot

# Update and install Python3
RUN apt-get update
RUN apt-get install -y python3 python3-pip
# Copy content
COPY . /root/

# Start installing
WORKDIR /root/
RUN pip3 install -r requirements.txt
RUN python3 setup.py install

# Mapping VOLUME
VOLUME ["/root/etc"]

# Running telebot
WORKDIR /root/etc/
CMD ["bot_mdt", "--config-file", "tele.conf"]
