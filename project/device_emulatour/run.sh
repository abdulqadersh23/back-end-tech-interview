#!/bin/bash
if ! [ -f $ENV ]; then
  echo "File $ENV does not exist."
  echo "copy .env-dev to .env `cp .env-dev .env` and edit value appropriately, Then re-run the script"
  exit 1
fi

base_dir=$PWD
ENV="${PWD}/.env"

  service="simple_device_emu"
  
  docker stop "$service" 2>/dev/null
  docker rm "$service" 2>/dev/null

  docker build --platform=linux/amd64 --network=host -f ./dockerfile -t "$service" .

  docker run -d \
    --name "$service" \
    -v /etc/localtime:/etc/localtime:ro \
    --env-file="$ENV" \
    --network="host" \
    --restart always \
    "$service"

  echo "Finished building $service"
  echo "-----------------------------"
