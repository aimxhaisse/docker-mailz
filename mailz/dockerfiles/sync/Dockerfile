FROM ubuntu:vivid
MAINTAINER Sébastien Rannou <mxs@sbrk.org> (@aimxhaisse)

RUN apt-get update -q -y			\
    && apt-get install -q -y			\
       python3					\
       opensmtpd				\
       openssl					\
    && apt-get clean

ADD sync.py /sync.py

ENTRYPOINT /sync.py
