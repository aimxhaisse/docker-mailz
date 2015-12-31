# Mailz, lots of mailz

# General notes.
#
# The start of all containers is always done after regenerating all
# configurations, this is done in a dedicated temporary container:
# 'sync', which parses config.ini, and exports generated
# configurations to the mails/data/confs directory. Configurations
# files are then mounted read-only in all containers.

CONFIG ?= config-prod.ini

# Here we attempt to resolve the privkey/cert path from config.ini so
# we can mount them in the 'sync' container. This is required so the
# 'sync' script can decide wether or not we need to regenerate
# certicates.

SYNC_PRIVKEY = $(shell awk -F '=' '// { if ($$1 == "privkey") { print $$2; } }' < $(CONFIG))
SYNC_CERT = $(shell awk -F '=' '// { if ($$1 == "cert") { print $$2; } }' < $(CONFIG))

ifneq ($(SYNC_PRIVKEY),)
	EXTRA_VOLUMES += -v $(shell readlink -f $(SYNC_PRIVKEY)):/privkey.pem
endif
ifneq ($(SYNC_CERT),)
	EXTRA_VOLUMES += -v $(shell readlink -f $(SYNC_CERT)):/cert.pem
endif

# We attempt to extract the backup directory specified in the
# configuration file, if none, use a default one.

BACKUP = $(shell awk -F '=' '// { if ($$1 == "backup") { print $$2; } }' < $(CONFIG))

ifeq ($(BACKUP),)
	BACKUP=mailz/backups
endif

# Enough for the trickeries.

all:	spawn

spawn: sync
	# we need to explicitely stop here because we want the regenerate configuration to be taken into account
	docker-compose -f mailz/data/confs/docker-compose.yml -p mailz stop
	docker-compose -f mailz/data/confs/docker-compose.yml -p mailz up -d

sync:
	docker build -t mailz_sync mailz/dockerfiles/sync
	docker run \
		-v $(shell pwd)/mailz/data/confs:/confs 	\
		-v $(shell pwd)/$(CONFIG):/config.ini 		\
		-v $(shell pwd)/mailz/templates:/templates	\
		$(EXTRA_VOLUMES)				\
		-e DEFAULT_HOSTNAME=$(shell hostname -f)	\
		-e DATA_DIR=$(shell pwd)/mailz/data/		\
		-e CONF_DIR=$(shell pwd)/mailz/data/confs/	\
		--rm --name mailz_sync_run mailz_sync

stop:
	docker-compose -f mailz/data/confs/docker-compose.yml -p mailz stop

logs:
	docker-compose -f mailz/data/confs/docker-compose.yml -p mailz logs

backup:
	docker-compose -f mailz/data/confs/docker-compose.yml -p mailz stop
	mkdir -p $(BACKUP)
	# hack to be root without using sudo, we need this because permissions of some files have special rights.
	docker run --rm -v $(shell pwd)/mailz/data:/data alpine tar -zcvf - /data > $(BACKUP)/docker-mailz-backup-$(shell date +%s).tar.gz
	docker-compose -f mailz/data/confs/docker-compose.yml -p mailz up -d

.PHONY: all sync spawn logs backup stop
