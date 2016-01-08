FROM ubuntu:vivid
MAINTAINER Sébastien Rannou <mxs@sbrk.org> (@aimxhaisse)

ENV DEBIAN_FRONTEND noninteractive
ENV ROUNDCUBE_TARBALL https://downloads.sourceforge.net/project/roundcubemail/roundcubemail/1.1.2/roundcubemail-1.1.2-complete.tar.gz

RUN apt-get update

RUN apt-get install -q -y							\
    apache2									\
    libapache2-mod-php5								\
    php5									\
    php-auth									\
    php-mail-mime								\
    php-mail-mimedecode								\
    php-net-smtp								\
    php-net-socket								\
    php5-intl									\
    php5-json									\
    php5-common									\
    php5-mcrypt									\
    php5-gd									\
    php5-pspell									\
    php-auth-sasl 								\
    php-crypt-gpg								\
    php5-sqlite									\
    sqlite3									\
    wget

RUN php5enmod mcrypt sqlite3

RUN wget $ROUNDCUBE_TARBALL -O /roundcube.tar.gz				\
 && tar -xf /roundcube.tar.gz -C /var/www					\
 && mv /var/www/roundcubemail-1.1.2 /var/www/roundcube				\
 && chown -R www-data:www-data /var/www/roundcube				\
 && rm /roundcube.tar.gz

ENTRYPOINT a2ensite roundcube							\
 ; a2dissite 000-default 							\
 ; . /etc/apache2/envvars 							\
 ; mkdir -p /var/www/roundcube/data/						\
 ; touch /var/www/roundcube/data/roundcube.db					\
 ; chown -R www-data:www-data /var/www/roundcube/data/				\
 ; rm -f /var/run/apache2/apache2.pid						\
 ; apache2ctl -e info -DFOREGROUND
