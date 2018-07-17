#!/bin/bash

ECHO "Shutting down Dallinger"
docker-compose stop
ECHO "Docker ps:"
ECHO "----------"
docker ps