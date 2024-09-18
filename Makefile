ifeq ($(shell test -e '.env' && echo -n yes),yes)
	include .env
endif

HELP_FUN = \
	%help; while(<>){push@{$$help{$$2//'options'}},[$$1,$$3] \
	if/^([\w-_]+)\s*:.*\#\#(?:@(\w+))?\s(.*)$$/}; \
    print"$$_:\n", map"  $$_->[0]".(" "x(20-length($$_->[0])))."$$_->[1]\n",\
    @{$$help{$$_}},"\n" for keys %help; \

APP_NAME = notimy


# parse additional args for commands

args := $(wordlist 2, 100, $(MAKECMDGOALS))
ifndef args
MESSAGE = "No such command (or you pass two or many targets to ). List of possible commands: make help"
else
MESSAGE = "Done"
endif

test: ##@Test Make testing
	$(MAKE) -C backend test

psql:##@Database Connect to database via psql
	psql -d $(POSTGRES_DB) -U $(POSTGRES_USER)

clear-logs:
	cd backend/logs/test && rm *.log
	cd backend/logs && rm *.log

run:
	docker compose up --build

run-prod:
	docker compose -f docker-compose-prod.yml up --build

key:
	openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 3650 -nodes -subj "/C=XX/ST=StateName/L=CityName/O=CompanyName/OU=CompanySectionName/CN=localhost" \
	&& mv cert.pem certs/cert.pem && mv key.pem certs/key.pem

env:
	cp .env.example .env

setup:
	make key
	make env

off-postgres:
	sudo systemctl stop postgresql

on-postgres:
	sudo systemctl stop postgresql


%::
	echo $(MESSAGE)

