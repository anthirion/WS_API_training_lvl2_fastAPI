#!/bin/bash

# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

# Install docker dependencies
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

# Check that the installation of Docker is successful
sudo docker run hello-world

# Install docker compose
sudo apt-get install docker-compose-plugin -y
# Check that the installation of Docker compose is successful
docker compose version

# A FAIRE EN PLUS DES COMMANDES CI-DESSUS
# AJOUTER UN FICHIER .ENV
# TOUTES LES COMMANDES DOCKER ET DOCKER-COMPOSE DOIVENT ETRE PRECEDEES DE SUDO

# Build the docker image
sudo docker build -t shopapi .