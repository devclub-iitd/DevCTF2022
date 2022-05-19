#!/bin/bash
up(){
  echo "Starting services..."
  pushd nginx
  sudo docker-compose up -d --build
  popd

  pushd web_1
  sudo docker-compose up -d --build
  popd

  pushd web_2
  sudo docker-compose up -d --build
  popd

  pushd web_3
  sudo docker-compose up -d --build
  popd

  pushd web_4
  sudo docker-compose up -d --build
  popd

  pushd web_5
  sudo docker-compose up -d --build
  popd

  pushd web_6
  sudo docker-compose up -d --build
  popd

  pushd web_7
  sudo docker-compose up -d --build
  popd

  pushd dev4
  sudo docker-compose up -d --build
  popd

}

down(){
  echo "Stopping services..."
  
  pushd web_1
  sudo docker-compose down
  popd

  pushd web_2
  sudo docker-compose down
  popd

  pushd web_3
  sudo docker-compose down
  popd

  pushd web_4
  sudo docker-compose down
  popd

  pushd web_5
  sudo docker-compose down
  popd

  pushd web_6
  sudo docker-compose down
  popd

  pushd web_7
  sudo docker-compose down
  popd

  pushd dev4
  sudo docker-compose down
  popd

  pushd nginx
  sudo docker-compose down
  popd

}

arg=${1:-up}
if [[ $arg == "up" ]]; then
  up;
else
  down; 
fi
