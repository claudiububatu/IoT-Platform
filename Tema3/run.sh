#! /bin/bash

sudo mkdir -p db/influxdb-storage
sudo mkdir -p db/grafana-storage

sudo chmod o+w db/grafana-storage

sudo docker stack rm sprc3
sudo ip link show | awk '/vx-/{print $2}' | while read -r iface; do sudo ip link delete "${iface%:}"; done

sudo docker-compose -f stack.yml build
sudo systemctl restart docker
sudo docker stack deploy -c stack.yml sprc3

sudo ip link show | awk '/vx-/{print $2}' | while read -r iface; do sudo ip link delete "${iface%:}"; done