FROM ubuntu:vivid
MAINTAINER Sébastien Rannou <mxs@sbrk.org> (@aimxhaisse)

RUN apt-get update -q -y			\
 && apt-get install -q -y spampd 		\
 && apt-get clean

ENTRYPOINT spamd --username debian-spamd	\
  	   	 --nouser-config 		\
		 --syslog stderr		\
		 --ip-address			\
	   	 --allowed-ips 0.0.0.0/0
