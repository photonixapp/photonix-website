#!/bin/sh
if [ "$ENV" = "dev" ]
then
  >&2 echo "Starting mkdocs server"
  mkdocs serve -a 0.0.0.0:8001
fi
