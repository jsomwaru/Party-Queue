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
rm media/q.db
adev runserver main.py --host 0.0.0.0 --port 80 --app-factory main   
