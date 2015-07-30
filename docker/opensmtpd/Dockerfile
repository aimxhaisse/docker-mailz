FROM ubuntu:vivid
MAINTAINER Sébastien Rannou <mxs@sbrk.org> (@aimxhaisse)

RUN apt-get update -q -y			\
 && apt-get install -q -y opensmtpd

ENTRYPOINT chown root /etc/ssl/certs/mail.crt	\
 && chown root /etc/ssl/private/mail.key	\
 && chmod 400 /etc/ssl/certs/mail.crt      	\
 && chmod 400 /etc/ssl/private/mail.key       	\
 && smtpd -v -d
