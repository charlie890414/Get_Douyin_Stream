FROM ubuntu

LABEL maintainer="charlie890414"

RUN ln -fs /usr/share/zoneinfo/Asia/Taipei /etc/localtime

RUN apt -qq update && \
    apt -qq install aria2 ffmpeg python3-pip nano -y

RUN pip3 install aria2p m3u8

WORKDIR /home

RUN useradd douyin

USER douyin

CMD aria2c --conf-path=./aria2.conf -D && python3 main.py