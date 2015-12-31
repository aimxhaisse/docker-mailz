FROM ubuntu:vivid
MAINTAINER Sébastien Rannou <mxs@sbrk.org> (@aimxhaisse)

RUN apt-get update -q -y			\
    && apt-get install -q -y			\
       opensmtpd				\
    && apt-get clean

ENTRYPOINT read -r -p "Enter the password you want to encrypt: " PASS	\
	   && smtpctl encrypt "$PASS"
