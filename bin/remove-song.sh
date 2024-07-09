#!/bin/bash
BASEURL="${2:-localhost}"

admin_pass=$(cat ../media/.admin_pass)
curl -vvv -X DELETE -H "X-AuthToken: $admin_pass"  http://$BASEURL/remove/$1 

if [ $? -gt 0 ]
then
  echo "There was an error removing song $1 in the queue."
  exit 1
else
  echo "Song $1 successfully removed."
  exit 0
fi
