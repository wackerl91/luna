#!/bin/sh
# Originally written by miko
# Modified by dodslaser
# Modified again by wackerl91 (support for launch args)

LAUNCHER_PATH=$1
HEARTBEAT_PATH=$2
GAME=$3
CONF_PATH=$4


sudo su osmc -c "sh $HEARTBEAT_PATH &" &
sudo su osmc -c "nohup openvt -c 7 -s -f sh $LAUNCHER_PATH \"${GAME}\" $CONF_PATH >/dev/null 2>&1 &" &

sudo openvt -c 7 -s -f clear

sleep 2

sudo su -c "systemctl stop mediacenter &" &

exit
