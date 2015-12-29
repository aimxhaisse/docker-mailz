# Mailz, lots of mailz

# We do things in two passes:
#
# - we spawn a 'sync' container to gen all configs files from config.ini
# - we then (re)spawn all services

# Here we attempt to resolve the privkey/cert path from config.ini so
# we can mount them in the 'sync' container. This is required so the
# 'sync' script can decide wether or not we need to regenerate
# certicates.

SYNC_PRIVKEY=$(shell awk -F '=' '// { if ($$1 == "privkey") { print $$2; } }' < config.ini)
SYNC_CERT=$(shell awk -F '=' '// { if ($$1 == "cert") { print $$2; } }' < config.ini)
BACKUP=$(shell awk -F '=' '// { if ($$1 == "backup") { print $$2; } }' < config.ini)

ifneq ($(SYNC_PRIVKEY),)
	EXTRA_VOLUMES += -v $(shell readlink -f $(SYNC_PRIVKEY)):/privkey.pem
endif
ifneq ($(SYNC_CERT),)
	EXTRA_VOLUMES += -v $(shell readlink -f $(SYNC_CERT)):/cert.pem
endif
ifeq ($(BACKUP),)
	BACKUP=mailz/backups
endif

# Enough for the trickeries.

all:	reload start

reload:
	docker build -t mailz_sync mailz/dockerfiles/sync
	docker run \
		-v $(shell pwd)/mailz/data/confs:/confs 							\
		-v $(shell pwd)/config.ini:/config.ini 								\
		-v $(shell pwd)/mailz/templates:/templates				 			\
		$(EXTRA_VOLUMES)										\
		-e DEFAULT_HOSTNAME=$(shell hostname -f)							\
		-e DATA_DIR=$(shell pwd)/mailz/data/								\
		-e CONF_DIR=$(shell pwd)/mailz/data/confs/							\
		--rm --name mailz_sync_run mailz_sync

start:
	docker-compose -f mailz/data/confs/docker-compose.yml -p mailz build
	docker-compose -f mailz/data/confs/docker-compose.yml -p mailz up -d

stop:
	docker-compose -f mailz/data/confs/docker-compose.yml -p mailz stop

backup:
	docker-compose -f mailz/data/confs/docker-compose.yml -p mailz stop
	mkdir -p $(BACKUP)
	# hack to be root without using sudo
	docker run --rm -v $(shell pwd)/mailz/data:/data alpine tar -zcvf - /data > $(BACKUP)/docker-mailz-backup-$(shell date +%s).tar.gz
	docker-compose -f mailz/data/confs/docker-compose.yml -p mailz up -d

.PHONY: backup start reload all stop
