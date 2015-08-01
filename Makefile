# Makefile used to initialize dockerz-mail
HOSTNAME 	?= $(shell hostname -f)

# Aliases
KEY_PRIV 	?= data/confs/mail.key
CRT_PUB  	?= data/confs/mail.crt
TPL_SMTPD	?= misc/smtpd.conf.template
CONF_SMTPD	?= data/confs/smtpd.conf
CONF_MAILNAME	?= data/confs/mailname
TPL_VHOST	?= misc/virtualhost.template
CONF_VHOST	?= data/confs/virtualhost.conf
CREDENTIALS	?= data/users.db
ROUNDCUBE	?= data/roundcube

all:	.first-init

.first-init: $(KEY_PRIV) $(CRT_PUB) $(CONF_SMTPD) $(CONF_MAILNAME) $(CREDENTIALS) $(ROUNDCUBE) $(CONF_VHOST)
	touch $@

$(KEY_PRIV):
	openssl genrsa -out $@ 4096
	chmod 700 $@

$(CRT_PUB):
	openssl req -new -x509 -key $(KEY_PRIV) -out $@
	chmod 700 $@

$(CONF_SMTPD): $(TPL_SMTPD)
	sed s/{hostname}/$(HOSTNAME)/g $(TPL_SMTPD) > $@

$(CONF_MAILNAME):
	echo $(HOSTNAME) > $@

$(CREDENTIALS):
	touch $@

$(ROUNDCUBE):
	mkdir -p $@
	chmod 775 $@

$(CONF_VHOST): $(TPL_VHOST)
	sed s/{hostname}/$(HOSTNAME)/g $(TPL_VHOST) > $@
