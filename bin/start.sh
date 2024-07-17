#!/bin/bash

pushd $(git rev-parse --show-toplevel)

pushd components/
id=$(docker ps --filter "name=redis" --format "{{.ID}}")

if [[ $OSTYPE =~ ^[darwin\d*] ]]
then
    if [ -z $id ]
    then
        echo "Starting redis"
        docker compose up -d redis
    else
        echo "Restarting redis"
        docker restart $id
    fi
    popd
    adev runserver partyq/main.py --host 0.0.0.0 --port 80 --app-factory main
elif [ $OSTYPE = "linux-gnu" ]
then
    docker compose up --force-recreate -d
    popd
    source $VIRTUAL_ENV/bin/activate
    adev runserver partyq/main.py --host 127.0.0.1 --port 8080 --app-factory main
fi 
