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
	export PYTHONPATH=$PYTHONPATH:$(pwd)/backend
	poetry run python -m pytest --verbosity=3 --showlocals --log-level=DEBUG

psql:##@Database Connect to database via psql
	psql -d $(POSTGRES_DB) -U $(POSTGRES_USER)

%::
	echo $(MESSAGE)
