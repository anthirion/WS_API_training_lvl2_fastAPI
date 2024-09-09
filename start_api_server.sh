#!/bin/bash

# GREEN='\033[0;32m'
# NC='\033[0m' # No Color

# wait until db container is up and a connection can be created
# the --strict argument executes the echo command only if the server is up
./wait-for-it/wait-for-it.sh db:3306 --strict -- echo "DB SERVER IS UP"
# launch the api on production mode
fastapi run app/main.py
# wait until api server is available on port 8000
./wait-for-it/wait-for-it.sh apiserver:8000 --strict -- echo "API SERVER IS UP"
