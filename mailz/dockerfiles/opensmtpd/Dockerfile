FROM ubuntu:vivid
MAINTAINER Sébastien Rannou <mxs@sbrk.org> (@aimxhaisse)

RUN apt-get update -q -y			\
 && apt-get install -q -y 			\
    opensmtpd					\
    ca-certificates				\
 && apt-get clean

ENTRYPOINT chown root /etc/ssl/mail.crt		\
 ; chmod 444 /etc/ssl/mail.crt      		\
 ; chown root /etc/ssl/private/mail.key		\
 ; chmod 400 /etc/ssl/private/mail.key       	\
 ; chown root /var/spool/smtpd			\
 ; chmod 711 /var/spool/smtpd			\
 ; chown opensmtpq /var/spool/smtpd/*		\
 ; chown root /var/spool/smtpd/offline		\
 ; rm -f /var/run/smtpd.pid			\
 ; newaliases					\
 ; smtpd -d
