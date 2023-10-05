#!/bin/bash
pushd components/
id=$(docker ps --filter "name=redis" --format "{{.ID}}")
if [ -n $id ]
then
    echo "Restarting redis"
    docker restart $id
else
    echo "Starting redis"
    docker compose up -d
fi
popd
./main.py