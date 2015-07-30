# Makefile used to initialize dockerz-mail
HOSTNAME 	?= sbrk.org

# Aliases
KEY_PRIV 	?= data/confs/mail.key
CRT_PUB  	?= data/confs/mail.crt
TPL_SMTPD	?= misc/smtpd.conf.template
CONF_SMTPD	?= data/confs/smtpd.conf
CONF_MAILNAME	?= data/confs/mailname
CREDENTIALS	?= data/users.db

all:	.first-init

.first-init: $(KEY_PRIV) $(CRT_PUB) $(CONF_SMTPD) $(CONF_MAILNAME) $(CREDENTIALS)
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
