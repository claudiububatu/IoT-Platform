#!/bin/bash

while [ 1 ]; do
    sudo nc -z sprc3_broker 1883 2> /dev/null \
    && sudo nc -z sprc3_influxdb 8086 2> /dev/null \
	&& break

    sleep 1;
done

sudo python3 -u server.py > /var/log/server.log 2>&1