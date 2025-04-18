#!/bin/bash
set -e

echo "Creating test user and test database..."

psql -v ON_ERROR_STOP=1 --username "${POSTGRES_USER}" --dbname "${POSTGRES_DB}" <<-EOSQL
  CREATE USER ${TEST_DATABASE_USER} WITH PASSWORD '${TEST_DATABASE_PASSWORD}';
  CREATE DATABASE ${TEST_DATABASE_NAME} OWNER ${TEST_DATABASE_USER};
  GRANT ALL PRIVILEGES ON DATABASE ${TEST_DATABASE_NAME} TO ${TEST_DATABASE_USER};
EOSQL
