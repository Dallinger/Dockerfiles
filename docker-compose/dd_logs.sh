#!/bin/bash

ECHO "Exporting logs..."
sleep 2
docker-compose logs dallinger |& tee log_dallinger.txt
docker-compose logs redis |& tee log_redis.txt
docker-compose logs postgresql |& tee log_postgresql.txt
ECHO
ECHO "Logs saved."