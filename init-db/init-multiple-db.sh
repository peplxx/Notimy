#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE notimy;
    CREATE DATABASE notimy_bot;
EOSQL
