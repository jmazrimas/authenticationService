#!/bin/bash

MODE=$1

stop_previous() {
  kill -9 $(pgrep -f flask)
  sudo docker stop authentication-server authentication-mariadb
  sudo docker rm authentication-server authentication-mariadb
}

stop_previous_db() {
  kill -9 $(pgrep -f flask)
  sudo docker stop authentication-mariadb
  sudo docker rm authentication-mariadb
}

start_db() {
  cd database
  sudo docker pull mariadb:latest
  sudo docker run --name authentication-mariadb -p 3306:3306 --env-file env_variables -d mariadb:latest

  sleep 15
  cat authentication-schema.sql | sudo docker exec -i authentication-mariadb /usr/bin/mysql -u authentication -p authenticationpass authentication
  cd ..
}

start_flask() {
  sudo docker build --build-arg google_oauth_client_id=60575523939-uecotuip3btkh66604hnk9o9gm6uiv9t.apps.googleusercontent.com --build-arg google_oauth_secret=XyhqeMKs86XXW1vGWxQB0Tq0 -t authentication-server .
  sudo docker run -d -p 8090:8090 authentication-server
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
elif [ "$MODE" == "dbonly" ]
then
  stop_previous_db
  start_db
else
  echo "USAGE: deploy.sh [MODE]"
  echo "MODE is either dev, debug, or prod"
fi
