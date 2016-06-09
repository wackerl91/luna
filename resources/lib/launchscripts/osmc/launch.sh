#!/bin/bash

GAME=$1
CONF_PATH=$2
DEBUG_ENABLED=$3
LOG_PATH="$(dirname ${CONF_PATH})/moonlight.log"

# taken from: http://stackoverflow.com/questions/420278/append-text-to-stderr-redirects-in-bash
foo() { while IFS='' read -r line; do echo "$(date) [INFO] $line" >> ${LOG_PATH}; done; };
foo_err() { while IFS='' read -r line; do echo "$(date) [ERROR] $line" >> ${LOG_PATH}; done; };

if test "${DEBUG_ENABLED}" = "true"; then
    moonlight stream -app "${GAME}" -config "${CONF_PATH}" > >(foo) 2> >(foo_err)
else
    moonlight stream -app "${GAME}" -config "${CONF_PATH}"
fi