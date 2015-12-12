#!/bin/sh

LAUNCHER_PATH=$1
GAME=$2
CONF_PATH=$3

sudo su osmc -c "nohup openvt -c 7 -s -f sh $LAUNCHER_PATH $GAME $CONF_PATH >/dev/null 2>&1 &" &
sudo openvt -c 7 -s -f clear

sleep 2

sudo su -c "systemctl stop mediacenter &" &
exit
