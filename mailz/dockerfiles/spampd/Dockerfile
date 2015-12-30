FROM ubuntu:vivid
MAINTAINER Sébastien Rannou <mxs@sbrk.org> (@aimxhaisse)

RUN apt-get update -q -y			\
 && apt-get install -q -y 			\
    spampd 					\
    libarchive-tar-perl				\
    libsys-syslog-perl				\
    rsyslog					\
 && apt-get clean

ENTRYPOINT rsyslogd ;				\
	   spampd --host 0.0.0.0:24		\
		  --relayhost dovecot:24	\
		  --user spampd			\
		  --group spampd		\
		  --nodetach  			\
		  --tagall			\
		  --debug			\
		  --config /etc/spampd.conf
