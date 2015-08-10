FROM ubuntu:vivid
MAINTAINER Sébastien Rannou <mxs@sbrk.org> (@aimxhaisse)

RUN apt-get update -q -y					\
 && apt-get install -q -y dovecot-imapd

ADD dovecot.conf /etc/dovecot/dovecot.conf

RUN groupadd -g 1000 vmail					\
 && useradd -g vmail -u 1000 vmail -d /var/vmail 		\
 && mkdir /var/vmail						\
 && chown vmail:vmail /var/vmail

ENTRYPOINT chown root /etc/pki/tls/certs/mail.crt		\
 ; chown root /etc/ssl/private/mail.key				\
 ; chmod 400 /etc/pki/tls/certs/mail.crt			\
 ; chmod 400 /etc/ssl/private/mail.key       			\
 ; dovecot -F
