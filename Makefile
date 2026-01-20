.PHONY: be-dev be-dev-ml be-dev-reset be-api-run be-db-fresh be-db-up be-db-down be-db-logs be-db-ps fe-install fe-dev fe-build fe-generate fe-docker-build fe-docker-up fe-docker-down fe-docker-logs fe-docker-ps fe-docker-dev docker-fresh

BE_DIR := MKJD_BE
FE_DIR := MKJD_FE
NPM ?= npm

be-dev:
	$(MAKE) -C $(BE_DIR) dev

be-dev-ml:
	$(MAKE) -C $(BE_DIR) dev-ml

be-dev-reset:
	$(MAKE) -C $(BE_DIR) dev-reset

be-api-run:
	$(MAKE) -C $(BE_DIR) api-run

be-db-fresh:
	$(MAKE) -C $(BE_DIR) docker-fresh

be-db-up:
	$(MAKE) -C $(BE_DIR) docker-up

be-db-down:
	$(MAKE) -C $(BE_DIR) docker-down

be-db-logs:
	$(MAKE) -C $(BE_DIR) docker-logs

be-db-ps:
	$(MAKE) -C $(BE_DIR) docker-ps

fe-install:
	$(NPM) --prefix $(FE_DIR) install

fe-dev:
	$(NPM) --prefix $(FE_DIR) run dev

fe-build:
	$(NPM) --prefix $(FE_DIR) run build

fe-generate:
	$(NPM) --prefix $(FE_DIR) run generate

fe-docker-build:
	$(MAKE) -C $(FE_DIR) docker-build

fe-docker-up:
	$(MAKE) -C $(FE_DIR) docker-up

fe-docker-down:
	$(MAKE) -C $(FE_DIR) docker-down

fe-docker-logs:
	$(MAKE) -C $(FE_DIR) docker-logs

fe-docker-ps:
	$(MAKE) -C $(FE_DIR) docker-ps

fe-docker-dev:
	$(MAKE) -C $(FE_DIR) docker-dev

docker-fresh:
	$(MAKE) -C $(BE_DIR) docker-fresh
	$(MAKE) -C $(FE_DIR) docker-fresh
