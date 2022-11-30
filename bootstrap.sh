#!/bin/bash

# run various pieces of initialization code here
# ...
echo "COMMAND" ${COMMAND}

init_app() {
    echo "Start it"
    cd /application/api
    python -m flask run --host 0.0.0.0
}

case "${COMMAND}" in
    init) init_app;;
    *) init_app;;
esac