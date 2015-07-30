FROM php:5.6-apache
MAINTAINER Sébastien Rannou <mxs@sbrk.org> (@aimxhaisse)

RUN apt-get update   		    \
 && apt-get install -q -y unzip

WORKDIR /var/www/html/

ENV SOURCE http://repository.rainloop.net/v2/webmail/rainloop-latest.zip
RUN curl -L -o rainloop.zip $SOURCE \
 && unzip rainloop.zip	    	    \
 && rm -rf rainloop.zip		    \
 && chown -R www-data .		    \
 && apt-get remove -y unzip
