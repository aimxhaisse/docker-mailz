# I systematically create all config files and respawn containers.

all:	configs

configs:
	docker build -t mailz_sync mailz/docker/sync
	docker run \
		-v $(shell pwd)/mailz/data/confs:/confs 					\
		-v $(shell pwd)/config.ini:/config.ini 						\
		-v $(shell pwd)/mailz/templates/smtpd.conf.template:/smtpd.conf.template 	\
		-v $(shell pwd)/mailz/templates/virtualhost.template:/virtualhost.template	\
		-e DEFAULT_HOSTNAME=$(shell hostname -f)					\
		--rm --name mailz_sync_run dockermailz_sync
