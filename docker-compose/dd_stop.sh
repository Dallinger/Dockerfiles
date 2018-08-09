#!/bin/bash
# Windows, MAC (OSX) and Ubuntu/Linux compatible version

ECHO "Shutting down Dallinger"
docker-compose stop
ECHO "Docker ps:"
ECHO "----------"
docker ps