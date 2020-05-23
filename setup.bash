#!/bin/bash
sudo apt-get update
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
sudo apt-get upgrade
if [ ! -x "$(command -v docker)" ]; then
    sudo apt install docker.io
    sudo systemctl enable --now docker
    docker --version
fi
if [ ! -x "$(command -v docker-compose)" ]; then
    sudo apt install docker-compose
    docker-compose version
fi
sudo docker-compose run -d --name mqtt mqtt
sleep 3
sudo docker exec "mqtt" sh -c "mosquitto_passwd -U ./passwd"
sudo docker-compose down
sudo docker-compose up -d
sudo docker ps -a
echo "Setup done!"