#!/bin/bash
# MAC (OSX) compatible version

ECHO "Shutting down Dallinger"
docker-compose stop
ECHO "Docker ps:"
ECHO "----------"
docker ps