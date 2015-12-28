#!/usr/bin/env bash

sleep 10

while [ true ]; do
        status="$(pidof moonlight | wc -w)"
        if [ ${status} -ne 1 ]; then
            sudo su -c "sudo systemctl restart mediacenter &" &
            exit
        else
            sleep 2
        fi
done
