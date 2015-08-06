FROM ubuntu:vivid
MAINTAINER Sébastien Rannou <mxs@sbrk.org> (@aimxhaisse)

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update

RUN ( echo "roundcube-core  roundcube/dbconfig-install      boolean true"	\
      echo "roundcube-core  roundcube/database-type select  sqlite3"; )		\
      | debconf-set-selections

RUN apt-get install -q -y							\
    roundcube-sqlite3								\
    roundcube-plugins		    						\
    roundcube-plugins-extra							\
    apache2

RUN php5enmod mcrypt sqlite3
RUN a2disconf roundcube

ADD main.inc.php /var/lib/roundcube/config/main.inc.php
RUN chown www-data /var/lib/roundcube/config/main.inc.php
RUN echo 'export DOCKERMAILZ_DOVECOT_1_PORT_993_TCP_ADDR' >> /etc/apache2/envvars

ENTRYPOINT a2ensite roundcube							\
 && a2dissite 000-default 							\
 && . /etc/apache2/envvars 							\
 && apache2ctl -D FOREGROUND
