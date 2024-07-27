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

# Commands
env:  ##@Environment Create .env file with variables
	@$(eval SHELL:=/bin/bash)
	@cp .env.example .env

help: ##@Help Show this help
	@echo -e "Usage: make [target] ...\n"
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

run: ##@Run Run from dockerfile
	docker run notimy

revision:  ##@Database Create new revision file automatically with prefix (ex. 2022_01_01_14cs34f_message.py)
	alembic revision --autogenerate

migrate: ##@Database Migrate head to last migration
	alembic upgrade head

test: ##@Test make testing
	cd tests && poetry run python -m pytest --verbosity=3 --showlocals --log-level=DEBUG

psql:##@Database Connect to database via psql
	psql -d $(POSTGRES_DB) -U $(POSTGRES_USER)

db:  ##@Database Create database with docker-compose
	docker-compose -f docker-compose.yml up -d --remove-orphans && docker-compose run db sh -c "alembic upgrade head"

db_down:  ##@Database Down database in docker container
	docker-compose -f docker-compose.yml down

db_startup:  ##@Database Startup database with migrations
	make db

build:
	docker build -t notimy .




%::
	echo $(MESSAGE)
