@echo off
setlocal enabledelayedexpansion

REM Set your Docker Hub credentials and image name
set DOCKER_USERNAME=abhishekak71
set IMAGE_NAME=akshopping-frontend
set STACK_NAME=my-app

REM Build the image
echo Building Docker image...
docker build -t %DOCKER_USERNAME%/%IMAGE_NAME% ./client

REM Push the image to Docker Hub
echo Pushing image to Docker Hub...
docker push %DOCKER_USERNAME%/%IMAGE_NAME%

REM Leave the swarm and reinitialize
echo Leaving swarm and reinitializing...
docker swarm leave --force
docker swarm init 

REM Deploy the stack
echo Deploying stack %STACK_NAME%...
docker stack deploy -c docker-compose.yml %STACK_NAME%
docker stack ls
echo Deployment completed!