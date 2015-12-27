# Mailz, lots of mailz

# Here we attempt to resolve the privkey/cert path from config.ini so
# we can mount them in the 'sync' container. This is required so the
# 'sync' script can decide wether or not we need to regenerate
# certicates.

SYNC_PRIVKEY=$(shell awk -F '=' '// { if ($$1 == "privkey") { print $$2; } }' < config.ini)
SYNC_CERT=$(shell awk -F '=' '// { if ($$1 == "cert") { print $$2; } }' < config.ini)

ifneq ($(SYNC_PRIVKEY),)
	EXTRA_VOLUMES += -v $(shell readlink -f $(SYNC_PRIVKEY)):/privkey.pem
endif
ifneq ($(SYNC_CERT),)
	EXTRA_VOLUMES += -v $(shell readlink -f $(SYNC_CERT)):/cert.pem
endif

# Enough for the trickeries, let's go

all:	configs reload

configs:
	docker build -t mailz_sync mailz/docker/sync
	docker run \
		-v $(shell pwd)/mailz/data/confs:/confs 							\
		-v $(shell pwd)/config.ini:/config.ini 								\
		-v $(shell pwd)/mailz/templates:/templates				 			\
		$(EXTRA_VOLUMES)										\
		-e DEFAULT_HOSTNAME=$(shell hostname -f)							\
		--rm --name mailz_sync_run mailz_sync

reload:
	touch mailz/data/users.db
	docker-compose -f mailz/data/confs/docker-compose.yml -p mailz build
	docker-compose -f mailz/data/confs/docker-compose.yml -p mailz up -d
