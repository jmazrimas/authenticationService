#!/bin/bash

MODE=$1

clean_docker() {
  sudo docker container prune
  sudo docker image prune
  sudo docker network prune
  sudo docker volume prune
}

stop_previous() {
  kill -9 $(pgrep -f flask)
  sudo docker stop authentication-server authentication-mariadb
  sudo docker rm authentication-server authentication-mariadb
}

# stop_previous_db() {
#   kill -9 $(pgrep -f flask)
#   sudo docker stop authentication-mariadb
#   sudo docker rm authentication-mariadb
# }

start_db() {
  cd database
  sudo docker build -t authentication-mariadb .
  sudo docker run --name authentication-mariadb --env-file ./env_variables.list -d authentication-mariadb
  cd ..
}

start_flask() {
  cd flask
  sudo docker build --build-arg google_oauth_client_id=60575523939-uecotuip3btkh66604hnk9o9gm6uiv9t.apps.googleusercontent.com --build-arg google_oauth_secret=XyhqeMKs86XXW1vGWxQB0Tq0 --build-arg auth_svc_db_name=authentication --build-arg auth_svc_db_user=authentication --build-arg auth_svc_db_pass=authenticationpass -t authentication-server .
  # sudo docker run --name authentication-server -d -link authentication-mariadb -p 8090:8090 authentication-server
  sudo docker run --name authentication-server -d -p 8090:8090 authentication-server
  cd ..
}

start_flask_debug() {
  cd flask/
  export FLASK_APP=app.py
  export FLASK_DEBUG=1
  flask run &
  cd ..
}

if [ "$MODE" == "dev" ]
then
  stop_previous
  # start_network
  start_db
  start_flask
elif [ "$MODE" == "debug" ]
then
  stop_previous
  # start_network
  start_db
  start_flask_debug
elif [ "$MODE" == "prod" ]
then
  stop_previous
  # start_network
  start_db
  start_flask
elif [ "$MODE" == "stop" ]
then
  stop_previous
elif [ "$MODE" == "clean" ]
then
  clean_docker
else
  echo "USAGE: deploy.sh [MODE]"
  echo "MODE is either dev, debug, or prod"
fi
