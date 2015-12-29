#!/bin/sh

GAME=$1
CONF_PATH=$2

moonlight stream -app "${GAME}" -config "${CONF_PATH}"
