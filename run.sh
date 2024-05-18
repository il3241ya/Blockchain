#!/bin/bash
set -e

echo "Docker compose up..."
docker compose up -d 

CONTAINER_NAME=$(docker-compose ps -q blockchain | xargs docker inspect --format '{{.Name}}' | sed 's/^\/\(.*\)$/\1/')

echo "Connecting to ${CONTAINER_NAME} container..."
docker attach $CONTAINER_NAME



