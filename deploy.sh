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

start_db() {
  cd database
  sudo docker build --build-arg auth_svc_root_db_pass=$AUTH_SVC_ROOT_DB_PASS --build-arg auth_svc_db_name=$AUTH_SVC_DB_NAME --build-arg auth_svc_db_user=$AUTH_SVC_DB_USER --build-arg auth_svc_db_pass=$AUTH_SVC_DB_PASS -t authentication-mariadb .
  sudo docker run --network=auth_net --name authentication-mariadb -d authentication-mariadb
  cd ..
}

start_flask() {
  cd flask
  sudo docker build  --build-arg google_oauth_client_id=$GOOGLE_OAUTH_CLIENT_ID --build-arg google_oauth_secret=$GOOGLE_OAUTH_SECRET --build-arg auth_svc_db_name=$AUTH_SVC_DB_NAME --build-arg auth_svc_db_user=$AUTH_SVC_DB_USER --build-arg auth_svc_db_pass=$AUTH_SVC_DB_PASS --build-arg current_server_url=$CURRENT_SERVER_URL -t authentication-server .
  sudo docker run --network=auth_net --name authentication-server -p 8090:8090 -d authentication-server
  cd ..
}

start_network() {
  sudo docker network create --driver bridge auth_net
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
  start_network
  start_db
  sleep 8
  start_flask
elif [ "$MODE" == "prod" ]
then
  stop_previous
  start_network
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
  echo "MODE is either dev, prod, stop or clean"
fi
