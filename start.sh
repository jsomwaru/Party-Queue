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

if [ $OSTYPE = "darwin" ] 
then
    adev runserver partyq/main.py --host 0.0.0.0 --port 80 --app-factory main   
elif [ $OSTYPE = "linux-gnu" ]
then
    VIRTUAL_ENV=/opt/actions-runner/partyq
    # PATH="$VIRTUAL_ENV/bin:$PATH"
    # export PATH
    sudo su
    source ~/partyq/bin/activate
    adev runserver partyq/main.py --host 0.0.0.0 --port 80 --app-factory main   
fi 