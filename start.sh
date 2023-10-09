#!/bin/bash
pushd components/
id=$(docker ps --filter "name=redis" --format "{{.ID}}")
if [ -z $id ]
then
    echo "Starting redis"
    docker compose up -d
else
    echo "Restarting redis"
    docker restart $id
fi
popd
./main.py
