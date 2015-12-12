#!/bin/sh

GAME=$1
CONF_PATH=$2

sudo moonlight stream -app ${GAME} -config ${CONF_PATH}
