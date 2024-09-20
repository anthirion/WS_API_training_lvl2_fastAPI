#!/bin/bash

# ATTENTION : variabiliser les @ IP

# retrieve useful script
# git clone https://github.com/vishnubob/wait-for-it.git
# chmod +x /home/anthirion/wait-for-it/wait-for-it.sh
# # wait until db container is up and a connection can be created
# # the --strict argument executes the echo command only if the server is up
# /home/anthirion/wait-for-it/wait-for-it.sh 34.76.26.208:3306 --strict -- echo "DB SERVER IS UP"
# source /home/anthirion/app/fastapi_venv/bin/activate
# # launch the api on production mode
# fastapi run /home/anthirion/app/main.py
# # wait until api server is available on port 8000
# /home/anthirion/wait-for-it/wait-for-it.sh localhost:8000 --strict -- echo "API SERVER IS UP"


# Activer l'environnement virtuel
source /home/anthirion/app/fastapi_venv/bin/activate
# Démarrer le serveur API en mode production
fastapi run /home/anthirion/app/main.py