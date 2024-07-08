#!/bin/bash

BASEURL={$2:localhost}

curl -X DELETE http://$BASEURL/remove/$1 
