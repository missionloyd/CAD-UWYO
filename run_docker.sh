#!/bin/bash
echo "setting development env variables in './.env.development'"
export DOCKER_COMPOSE_ENV_FILE=./.env.development

echo "building docker containers"
docker-compose --env-file $DOCKER_COMPOSE_ENV_FILE build --force-rm --no-cache && docker-compose --env-file $DOCKER_COMPOSE_ENV_FILE up --detach && docker-compose --env-file $DOCKER_COMPOSE_ENV_FILE logs --follow
