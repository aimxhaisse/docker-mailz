FROM ubuntu:vivid
MAINTAINER Sébastien Rannou <mxs@sbrk.org> (@aimxhaisse)

RUN apt-get update -q -y			\
 && apt-get install -q -y dovecot-imapd

ADD dovecot.conf /etc/dovecot/dovecot.conf

ENTRYPOINT chown root /etc/ssl/certs/mail.crt	\
 && chown root /etc/ssl/private/mail.key	\
 && chmod 400 /etc/ssl/certs/mail.crt      	\
 && chmod 400 /etc/ssl/private/mail.key       	\
 && dovecot -F
