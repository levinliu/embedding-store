#!/bin/bash

function init_app() {
    cd /app
    if [ -e "./init_app.sh" ] ; then
        bash ./init_app.sh
    else
        echo "no init app script, do nothing"  > not_init.log
    fi
}

init_app &

sleep 36000000