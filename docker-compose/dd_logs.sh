#!/bin/bash
# MAC (OSX) compatible version

ECHO "Exporting logs..."
sleep 2
docker-compose logs dallinger >& log_dallinger.txt
docker-compose logs redis >& log_redis.txt
docker-compose logs postgresql >& log_postgresql.txt
ECHO
ECHO "Logs saved."