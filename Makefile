.PHONY: be-dev be-dev-ml be-api-run be-db-fresh be-db-up be-db-down be-db-logs be-db-ps fe-install fe-dev fe-build fe-generate

BE_DIR := MKJD_BE
FE_DIR := MKJD_FE
NPM ?= npm

be-dev:
	$(MAKE) -C $(BE_DIR) dev

be-dev-ml:
	$(MAKE) -C $(BE_DIR) dev-ml

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
