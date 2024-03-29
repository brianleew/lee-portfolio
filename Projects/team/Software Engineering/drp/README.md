# DRP - Demand Response Portal
===========================================

## Infrastructure
-------------------------------------------
Ran in https://vcenterceroc.tntech.edu/

MySQL database: https://hub.docker.com/_/mysql

Flask Website: https://blog.logrocket.com/build-deploy-flask-app-using-docker/

## Build
-------------------------------------------
Prerequisites: docker installed

Navigate to drp/src/ directory and run following command to start the containers. 

    sudo docker compose up --build 

To take down the docker containers, use the following command. 

    sudo docker compose down
