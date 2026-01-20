.PHONY: docker-build docker-up docker-down docker-logs docker-ps docker-restart docker-dev docker-fresh

COMPOSE ?= docker compose

docker-build:
	$(COMPOSE) build

docker-up:
	$(COMPOSE) up -d

docker-dev:
	$(COMPOSE) up

docker-down:
	$(COMPOSE) down

docker-restart:
	$(COMPOSE) restart

docker-logs:
	$(COMPOSE) logs -f

docker-ps:
	$(COMPOSE) ps

docker-fresh:
	$(COMPOSE) down -v
	$(COMPOSE) build
	$(COMPOSE) up -d
