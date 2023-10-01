#!/bin/bash

# !!!! WARNING !!!! #
# if you change this file you need to delete pg-scripts volume in order
# to be redeployed

set -e

function create_user_and_database() {
	local database=$1
  local user=$2
	echo  && echo "Creating user '$user' and database '$database'" && echo
  sleep 100

	createdb -U postgres -O "$user" "$database"
}

# These environment values are taken from .env and docker-compose
if [ -n "$POSTGRES_DB" ]; then
  if [ -n "$POSTGRES_USER" ]; then
    user=$POSTGRES_USER
  else
    user=postgres  # default
  fi

  create_user_and_database "$POSTGRES_DB" "$user"
  echo "User and database ${POSTGRES_DB} created"
else
  echo Warning: POSTRGRES_DB environment variable is not set
  echo Therefore not taking any further custom action on db container
fi
