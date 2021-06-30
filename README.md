# 2021 Bootcamp CI/CD & Docker (pt. 1)

<!-- TOC -->

- [Bootcamp CI/CD & Docker pt. 1](#bootcamp-cicd--docker-pt-1)
    - [Introduction to Docker](#introduction-to-docker)
        - [What is Docker?](#what-is-docker)
        - [Why use Docker?](#why-use-docker)
        - [What does a Docker Image look like?](#what-does-a-docker-image-look-like)
    - [How do I use Docker images?](#how-do-i-use-docker-images)
        - [Install Docker](#install-docker)
        - [Pull the Redis image](#pull-the-redis-image)
        - [Inspect the Redis image](#inspect-the-redis-image)
    - [Deploying an Open Source image](#deploying-an-open-source-image)
        - [Create Redis container](#create-redis-container)
        - [View Redis in container list](#view-redis-in-container-list)
        - [Check Redis Logs](#check-redis-logs)
        - [Store data in Redis](#store-data-in-redis)
        - [Get data from Redis](#get-data-from-redis)
        - [Stop Redis container](#stop-redis-container)
        - [Try to get data again](#try-to-get-data-again)
        - [Start the stopped Redis container](#start-the-stopped-redis-container)
        - [Try to get data again data is preserved](#try-to-get-data-again-data-is-preserved)
        - [Remove Redis container](#remove-redis-container)
        - [Recreate and see that the data doesn't exist anymore](#recreate-and-see-that-the-data-doesnt-exist-anymore)
    - [Using Docker Volumes to preserve container data](#using-docker-volumes-to-preserve-container-data)
        - [Create Redis data volume](#create-redis-data-volume)
        - [Recreate Redis container, using a docker volume](#recreate-redis-container-using-a-docker-volume)
        - [Enter Redis container, using interactive session](#enter-redis-container-using-interactive-session)
        - [Delete Redis container](#delete-redis-container)
        - [Recreate the Redis container, using the same docker volume](#recreate-the-redis-container-using-the-same-docker-volume)
        - [Validate data persistence](#validate-data-persistence)
    - [Create custom Docker images](#create-custom-docker-images)
        - [Build our image](#build-our-image)
        - [Run our image](#run-our-image)
            - [Run our image with a different CMD](#run-our-image-with-a-different-cmd)
        - [Connect Docker Containers](#connect-docker-containers)
            - [docker network create](#docker-network-create)
            - [docker network connect](#docker-network-connect)
            - [docker inspect redis](#docker-inspect-redis)
            - [docker run --net](#docker-run---net)
        - [Talking to Redis](#talking-to-redis)
            - [Run a single command](#run-a-single-command)
            - [Run a command that creates a shell](#run-a-command-that-creates-a-shell)
                - [Validate the stored data](#validate-the-stored-data)
    - [Speeding things up with Docker Compose](#speeding-things-up-with-docker-compose)
        - [docker-compose files](#docker-compose-files)
        - [docker-compose cli](#docker-compose-cli)
            - [docker-compose up](#docker-compose-up)
            - [docker-compose ps](#docker-compose-ps)
            - [docker-compose exec](#docker-compose-exec)
                - [Side note](#side-note)
                - [Living inside a container](#living-inside-a-container)
            - [docker-compose down](#docker-compose-down)
    - [Final Thoughts](#final-thoughts)

<!-- /TOC -->

## Introduction to Docker

> The goal of this bootcamp exercise is to provide an overview of one of the newer components of CI/CD: containers.

### What is Docker?

![That's a big question](https://31.media.tumblr.com/a4a72524f0bc49663881898367b5246a/tumblr_ns8pm9eEwN1tq4of6o1_540.gif)

In their own words:

> Developing apps today requires so much more than writing code. Multiple languages, frameworks, architectures, and discontinuous interfaces between tools for each lifecycle stage creates enormous complexity. Docker simplifies and accelerates your workflow, while giving developers the freedom to innovate with their choice of tools, application stacks, and deployment environments for each project.

Essentially, 

- Docker is a tool that allows you to package code into a Docker image (a re-usable file used to execute code in a Docker container).
- Docker images are the blueprint for Docker containers, which are isolated execution environments.

### Why use Docker?

- Docker is a standard package that works across multiple architectures and environment type. i.e. Build a single Docker image that would run the same on Windows vs Mac. 
- Integrate with popular [open-source solutions](https://hub.docker.com/search?q=&type=image) for databases, caching, monitoring, gaming, and more.
- Since each container is isolated by default, the security from Docker can be unparallelled. For example, consider a web appliction that runs inside of a container. If the application was compriomised by bad actors, they'd only have access to the contents of the container, and not the entire host filesystem.
- [So much more...](https://www.docker.com/use-cases)

### What does a Docker Image look like?

Let's take a look at the [Docker docs](https://docs.docker.com/language/python/build-images/#create-a-dockerfile-for-python) for creating a `Dockerfile` for a python application.

```Docker
FROM python:3.8-slim-buster
# What is our base image? Since we want to create a python application, we need a base image that has python. Luckily, we can continue making use of open-source images for this as well. There are many types of images that provide python, but for this example i'll choose 

WORKDIR /app
# What directory (inside the container) should we be working from?

COPY requirements.txt requirements.txt
# Copy over the project requirements

RUN pip3 install -r requirements.txt
# Run a command to install the requirements

COPY . .
# Copy over the rest of the app

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
# What should the main command of this container be? If this command exits, the container exits.
```

## How do I use Docker images?

Each image is different in terms of how you configure the specifics for the application running inside. What's common though, is _how_ you configure the containers. Most images are configured using environment variables and/or by mounting a local Docker volume with configuration files present. 

Let's look at Redis, as it's a very popular and useful key-value store and caching solution.

### Install Docker
To [install Docker](https://docs.docker.com/docker-for-mac/install/), download the DMG file from: https://desktop.docker.com/mac/stable/amd64/Docker.dmg

From their docs:

1. Double-click `Docker.dmg` to open the installer, then drag the Docker icon to
    the Applications folder.

      ![Install Docker app](https://docs.docker.com/docker-for-mac/images/docker-app-drag.png)

2. Double-click `Docker.app` in the Applications folder to start Docker. (In the example below, the Applications folder is in "grid" view mode.)

    ![Docker app in Hockeyapp](https://docs.docker.com/docker-for-mac/images/docker-app-in-apps.png)

    The Docker menu in the top status bar indicates that Docker Desktop is running, and accessible from a terminal.

      ![Whale in menu bar](https://docs.docker.com/docker-for-mac/images/whale-in-menu-bar.png)

    If you've just installed the app, Docker Desktop launches the onboarding tutorial. The tutorial includes a simple exercise to build an example Docker image, run it as a container, push and save the image to Docker Hub.

    ![Docker Quick Start tutorial](https://docs.docker.com/docker-for-mac/images/docker-tutorial-mac.png)

3. Click the Docker menu (![whale menu](https://docs.docker.com/docker-for-mac/images/whale-x.png)) to see
**Preferences** and other options.

4. Select **About Docker** to verify that you have the latest version.

Congratulations! You are now successfully running Docker Desktop.

### Pull the Redis image

All we need to do is type `docker pull REPOSITORY[:TAG]`. What does this syntax mean? Well docker images are stored in repositories, just like code is stored in git repositories. By default, all images are pulled from DockerHub. You are able to create and manage your own image repositories, but we won't go over that. The image repository is required, but the tag isn't and will be defaulted to `latest` if nothing is given for it.

```bash
$ docker pull redis

Using default tag: latest
latest: Pulling from library/redis
Digest: sha256:7e2c6181ad5c425443b56c7c73a9cd6df24a122345847d1ea9bb86a5afc76325
Status: Image is up to date for redis:latest
docker.io/library/redis:latest
```

### Inspect the Redis image

To view the image details, we just need to type `docker images [REPOSITORY[:TAG]]`. This time, the repository is not required, but we are going to use it to limit our results to the image we want. For example:

```bash
$ docker images redis

REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
redis        latest    fad0ee7e917a   2 weeks ago   105MB
```

## Deploying an Open Source image

### Create Redis container
```bash
# Run the open-source image redis image (last arg), call it 'redis' (--name redis) and run it in detached mode (-d)
$ docker run --name redis -d redis:latest

<docker_image_id>
```

### View Redis in container list
```bash
# Check the status of the container
$ docker ps

CONTAINER ID   IMAGE          COMMAND                  CREATED          STATUS          PORTS      NAMES
16ad2cca6925   redis:latest   "docker-entrypoint.s…"   22 seconds ago   Up 21 seconds   6379/tcp   redis
```

### Check Redis Logs
```bash
$ docker logs redis

1:C 21 Jun 2021 19:21:53.171 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
1:C 21 Jun 2021 19:21:53.171 # Redis version=6.2.4, bits=64, commit=00000000, modified=0, pid=1, just started
1:C 21 Jun 2021 19:21:53.171 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
1:M 21 Jun 2021 19:21:53.172 * monotonic clock: POSIX clock_gettime
1:M 21 Jun 2021 19:21:53.172 * Running mode=standalone, port=6379.
1:M 21 Jun 2021 19:21:53.172 # Server initialized
1:M 21 Jun 2021 19:21:53.173 * Ready to accept connections
```

### Store data in Redis
```bash
# Read the following command like:

# docker Execute -i (interactive) -t (use a pseudo-TTY) redis (container name) redis-cli (command to run inside container) SET myname Andrew (arguments for the command ie. redis-cli)

$ docker exec -it redis redis-cli SET myname Andrew

OK
```

### Get data from Redis
```bash
$ docker exec -it redis redis-cli GET myname

"Andrew"
```

### Stop Redis container
```bash
$ docker stop redis

redis
```

### Try to get data again
```bash
$ docker exec -it redis redis-cli GET myname

Error response from daemon: Container <id> is not running
```

### Start the stopped Redis container
```bash
$ docker start redis

redis
```

### Try to get data again (data is preserved)

When you try to get the data again, this time, we see that the data is still there.

```bash
$ docker exec -it redis redis-cli GET myname

"Andrew"
```

### Remove Redis container

Finally, remove the container which will destroy the data inside of redis and remove the container from `docker ps`.

> remember to stop the container before attempting to removing!

```bash
$ docker rm redis

redis
```

### Recreate and see that the data doesn't exist anymore

```bash
$ docker run --rm --name redis -d redis:latest && docker exec -it redis redis-cli GET myname; docker stop redis;

(nil)
```

## Using [Docker Volumes](https://docs.docker.com/storage/volumes/) to preserve container data

In modern container orchestration technologies such as Kubernetes or Docker-Swarm, it's extremely common for containers to be removed and replaced with a different container. These two containers will have different ids, but they run the same application. As we just saw, when a container is removed it's data is also removed... so how can we make sure that the Redis data isn't deleted when the container is deleted?

> Docker Volumes allow you to map directories and files from the host os into the container os. 

### Create Redis data volume
```bash
# Run the open-source image redis image (last arg), call it 'redis' (--name redis) and run it in detached mode (-d)
$ docker volume create redis_data

redis_data
```

### Recreate Redis container, using a docker volume
```bash
# Run the open-source image redis image (last arg), call it 'redis' (--name redis) and run it in detached mode (-d) with volume 'redis_data'
$ docker run -v redis_data:/data --name redis -d redis:latest 

<docker_image_id>
```

### Enter Redis container, using interactive session

Let's create some data, then exit the container.

```bash
$ docker exec -it redis redis-cli

127.0.0.1:6379> SET myname Andrew
OK
127.0.0.1:6379> SET moredata potato
OK
127.0.0.1:6379> exit
```

Make sure the data exists, then exit the container.

```bash
$ docker exec -it redis redis-cli

127.0.0.1:6379> GET myname
"Andrew"
127.0.0.1:6379> GET moredata
"potato"
127.0.0.1:6379> exit
```

### Delete Redis container

```bash
$ docker stop redis && docker rm redis

redis
redis
```

### Recreate the Redis container, using the same docker volume

```bash
$ docker run -v redis_data:/data --name redis -d redis:latest

<id>
```

### Validate data persistence

```bash
$ docker exec -it redis redis-cli GET myname

"Andrew"
```

## Create custom Docker images

Let's create a container to utilize the code in `python-app/redis_client.py`. Our image is going to look very similar to the one we viewed earlier. With [Dockerfiles](/python-app/Dockerfile), it's extremely important to put the things that change _least_ at the top, as Docker will build and cache the `layers` it generates from this file. This is so that on subsequent builds, you won't need to wait for the entire command again (unless you explicitly want to run it without cache, which is possible). 

```Docker
# Use the small python image, no need for fancy add-ons
FROM python:3.8-slim-buster

# Use /app as our working directory
WORKDIR /app

# Copy our requirements
COPY requirements.txt requirements.txt

# Install our requirements
RUN pip3 install -r requirements.txt

# Copy the rest of our project
COPY . .

# Run our app
ENTRYPOINT [ "python3", "redis_client.py"]
```

Using this image, we can build a container that can run our app on almost any machine with that has Docker installed. 

> Question to think about: Why would we copy over the requirements file first, before copying over the rest of the app?

### Build our image

```bash
# Build our container and tag (name) it as "bootcamp". The `python-app` tells docker what context to use for building the image. In this case we want to be inside of the folder that has our code.
$ docker build -f python-app/Dockerfile -t bootcamp python-app
```
Let's run our code without arguments to see what it can do

### Run our image

```bash
$ docker run bootcamp

NAME
    redis_client.py

SYNOPSIS
    redis_client.py COMMAND

COMMANDS
    COMMAND is one of the following:

     store_data

     get_data

     check_redis
```

#### Run our image with a different `CMD`
Alright now that our container is running, let's just make sure we can connect to Redis with `check_redis`.

```bash
$ docker run bootcamp check_redis

...
  File "/usr/local/lib/python3.8/site-packages/redis/connection.py", line 1192, in get_connection
    connection.connect()
  File "/usr/local/lib/python3.8/site-packages/redis/connection.py", line 563, in connect
    raise ConnectionError(self._error_message(e))
redis.exceptions.ConnectionError: Error -2 connecting to redis:6379. Name or service not known.
```

> Doh! What's going on? Well remember how everything is isolated, this is actually a good thing. You need to explicitly tell docker that these containers can communicate with eachother. To do this, we need to create a Docker Network.

### Connect Docker Containers

#### docker network create
Create a docker network to act as an network environment for multiple containers.

```bash
$ docker network create bootcamp_net --attachable

<id>
```

#### docker network connect
Okay now that we have a network, let's attach our redis container to it.

```bash
$ docker network connect bootcamp_net redis --alias redis

...
```

#### docker inspect redis
Not the greatest output for this command so let's check it manually. 

```bash
$ docker inspect redis

...
            "IPv6Gateway": "",
            "MacAddress": "",
            "Networks": {
                "bootcamp_net": {
                    "IPAMConfig": {},
                    "Links": null,
                    "Aliases": [
                        "redis",
...
```

#### docker run --net
That's what we're looking for. Okay cool, now we need to run our container with this network as well.

```bash
$ docker run --net bootcamp_net bootcamp check_redis

True
```

### Talking to Redis
Yay! Now we can connect to redis from our other container. Let's check on that data from earlier:

#### Run a single command
```bash
$ docker run -t --net  bootcamp_net bootcamp get_data myname

The data is in redis!
key='myname'
val='Andrew'
```

#### Run a command that creates a shell
We can also store new data using an interactive shell (`-i`):

```bash
$ docker run -it --net  bootcamp_net bootcamp store_data

What should we call this data?
thebestfood
What is the data?
potato
The data has been stored in redis
 ```

##### Validate the stored data
Now let's check for that new data:

```bash
$ docker run -t --net  bootcamp_net bootcamp get_data thebestfood

The data is in redis!
key='thebestfood'
val='potato'
```

> Hopefully through this exercise you can see that docker can unlock some amazing development power, while remaining a secure platform to build and run containers from.

## Speeding things up with Docker Compose

So far it's kind of been a nightmare of cli commands. There has to be a better way right...?

There is! With docker-compose, we can combine everything we've learned so far into a single file that's easier to manage.
### docker-compose files

The `docker-compose.yml` file has it's own syntax, syntax verions, and a [ton of useful tools](https://docs.docker.com/compose/compose-file/compose-file-v3/) that we won't have time to go over here.

Here's what [a docker-compose.yml file](/python-app/docker-compose.yml) looks like: 

```bash
# The syntax version of docker-compose to use
version: "3.8"

# Create the network so that our containers can talk to eachother
networks:
    redis:
      name: redis_net
      driver: bridge

# Create the storage volume for redis
volumes: 
    redis_storage:
        name: redis_storage

# Define our containers
services:

    # Define redis properties
    cache:
        image: 'redis:latest'
        volumes: 
            - redis_storage:/data
        networks:
            - redis

    # Define python app properties, have it build our image
    app:
        build: 
            context: .
        networks: 
            - redis
        entrypoint: "/bin/sh"
        tty: yes
        healthcheck:
            test: ["CMD", "python", "redis_client.py", "check_redis"] 
            interval: 3s
```

### docker-compose cli

#### docker-compose up
The following command will create the network, the volume, both containers (in the background), and the proper links:

```bash
$ cd python-app
$ docker-compose up -d --build

...
Starting redis_app_1   ... done
Starting redis_cache_1 ... done
```

#### docker-compose ps
Let's check on it! Run the following command to see the status of everything:

```bash
$ docker-compose ps
    Name                   Command                  State        Ports  
------------------------------------------------------------------------
redis_app_1     /bin/sh                          Up (healthy)           
redis_cache_1   docker-entrypoint.sh redis ...   Up             6379/tcp
```

> The `Healthy` status above indicates that the command we defined as the healthcheck is returning without failing.

#### docker-compose exec
Now let's run our commands again, this time from inside the container! The following command will attach us to the python container so that we can run the same commands as before. We read this command like so: `docker execute <service_name> <command_inside_container>`.

```bash
$ docker-compose exec app /bin/sh
```

##### Side note

Most docker-contains have some type of shell that you can use to run commands with. In this case, the command we want to run will open up a new shell instance `/bin/sh` and attach us to it so that it acts as our new shell. When we are done, we exit it with `exit`. You could replace `/bin/sh` with any valid executable in the `$PATH` environment variable. For example, listing the files in the `WORKDIR` directory of a container:

```bash

$ docker-compose exec app ls -lrt

total 16
-rw-r--r-- 1 root root   48 Jun 21 18:56 requirements.txt
-rw-r--r-- 1 root root  361 Jun 21 20:46 Dockerfile
-rw-r--r-- 1 root root  797 Jun 21 23:04 docker-compose.yml
-rw-r--r-- 1 root root 1094 Jun 21 23:06 redis_client.py
```

##### Living inside a container
Now you are inside of the container, feel free to take a look around. When you are ready, run the `ENTRYPOINT` command:

```
$ python redis_client.py

NAME
    redis_client.py

SYNOPSIS
    redis_client.py COMMAND

COMMANDS
    COMMAND is one of the following:

     store_data

     get_data

     check_redis

---

$ python redis_client.py check_redis

True
```

Exit the container context by typing:

```bash
$ exit
```

#### docker-compose down
To bring all the containers down, type: 

Exit the container context by typing:

```bash
$ docker-compose down
```

> As you can see, docker compose drastically reduces development time while allowing the same features as the CLI.

## Final Thoughts

By going through this excercise, you should have a better idea of what Docker is and what kinds of things you can do with it. There is so much more to explore, here are just a few things that i've found fun while working with it:

- You can run Docker inside Docker (woah).
  - Very useful for CI/CD, since the runner can be containerized but it can also create other containers.
- Orchestrating container deployments with docker-compose using docker-swarm.
- *Using PyCharm to have your default interpreter be inside of a container*
  - Allows for a clean development environment on ever build
  - Debugging features still work
  - Easily test across python versions, by using a different base image for each build/test
  - More info: https://www.jetbrains.com/help/pycharm/using-docker-compose-as-a-remote-interpreter.html

I strongly believe that containers are the future, so this knowledge is going to be foundational before long. Any time you need a new software service, application, development environment, cicd runners, etc. just think `what i'm doing is probably a container, and it'll be easier to just use the container`.
