#! /bin/bash

prodname=$1
period=$2
pass=$3
runMin=
runMax=

if [ $# -eq 5 ]; then
    runMin=$4
    runMax=$5
fi

TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjU2NDA5OCIsInVzZXJuYW1lIjoiYWZlcnJlcm8iLCJuYW1lIjoiQW5kcmVhIEZlcnJlcm8iLCJhY2Nlc3MiOiJkZWZhdWx0LXJvbGUsYWRtaW4sZ3Vlc3QsZGV0LWNwdixkZXQtZW1jLGRldC1mZGQsZGV0LWZ0MCxkZXQtZnYwLGRldC1nbG8sZGV0LWhtcCxkZXQtaXRzLGRldC1tY2gsZGV0LW1mdCxkZXQtbWlkLGRldC1waHMsZGV0LXRvZixkZXQtdHBjLGRldC10cmQsZGV0LXpkYyIsImlhdCI6MTczNDYxMDk1NSwiZXhwIjoxNzM1MjE1NzU1LCJpc3MiOiJvMi11aSJ9.9o7rcbRcMcVv3R7_Jsn4A9iTG9HA6tEXWHnniTqnOQ4"

JQ_COMMAND=".token |= \"$TOKEN\" | del(.dataPassNames) | . += { dataPassNames }"
if [ -z "$runMin" ]; then
    JQ_COMMAND+=" | .dataPassNames += { $prodname: {} }"
else
    JQ_COMMAND+=" | .dataPassNames += { $prodname: { run_range: [$runMin,$runMax] } }"
fi

jq "${JQ_COMMAND}" config_rct.json > config_rct_temp.json
#cat config_rct_temp.json
python3 rct.py config_rct_temp.json

jq ".period |= \"$period\" | .pass |= \"$pass\"" rct_runlist.json > rct_runlist_temp.json
#cat rct_runlist_temp.json
python3 rct_runlist.py rct_runlist_temp.json
