FRESH DEVELOPMENT ENVIRONMENT SETUP

1. download and install docker desktop and have it running
2. cd Desktop/SE-DRP/drp/src -- this is an example. cd into ../drp/src
(now you are at src directory that has the files "example.env" and "docker-compose.yml")
3. change example.env to .env
4. then do `docker compose up -d --build`
Now, you should be able to go to `localhost` on your web browser to see DRP website

If database code is updated, delete the "data" folder in "src" directory,
while cd into src, make sure .env is setup correctly
run `docker compose down -v` deletes volume and servers from docker desktop
finally run `docker compose up -d --build`