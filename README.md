# 2021 Bootcamp CI/CD & Docker (pt. 1)



## Introduction to Docker

> The goal of this bootcamp exercise is to provide an overview of one of the newer components of CI/CD: containers.

### What is Docker?

![That's a big question](https://31.media.tumblr.com/a4a72524f0bc49663881898367b5246a/tumblr_ns8pm9eEwN1tq4of6o1_540.gif)

In their own words:

> Developing apps today requires so much more than writing code. Multiple languages, frameworks, architectures, and discontinuous interfaces between tools for each lifecycle stage creates enormous complexity. Docker simplifies and accelerates your workflow, while giving developers the freedom to innovate with their choice of tools, application stacks, and deployment environments for each project.

Essentially, 

- Docker is a tool that allows you to package code into a re-usable Docker image. 
- Docker images are the blueprint for Docker containers, which are isolated execution environments.

### Why use Docker?

- Docker a standard package that works across multiple architectures and environment type. i.e. Build a single Docker image that would run the same on Windows vs Mac. 
- Integrate with popular [open-source solutions](https://hub.docker.com/search?q=&type=image) for databases, caching, monitoring, gaming, and more.
- Since each container is isolated by default, the security from Docker can be unparallelled. For example, consider a web appliction that runs inside of a container. If the application was compriomised by bad actors, they'd only have access to the contents of the container, and not the entire host filesystem.
- [So much more...](https://www.docker.com/use-cases)

### What does a Docker Image look like?

Let's take a look at the [Docker docs](https://docs.docker.com/language/python/build-images/#create-a-dockerfile-for-python) for creating a `Dockerfile` for a python application.

```Docker
# What is our base image? Since we want to create a python application, we need a base image that has python. Luckily, we can continue making use of open-source images for this as well. There are many types of images that provide python, but for this example i'll choose 
FROM python:3.8-slim-buster

# What directory (inside the container) should we be working from?
WORKDIR /app

# Copy over the project requirements
COPY requirements.txt requirements.txt

# Run a command to install the requirements
RUN pip3 install -r requirements.txt

# Copy over the rest of the app
COPY . .

# What should the main command of this container be? If this command exits, the container exits.
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
```

## How do I use Docker images?

Each image is different in terms of how you configure the specifics for the application running inside. What's common though, is _how_ you configure the containers. Most images are configured using environment variables and/or by mounting a local Docker volume with configuration files present. 

Let's continue looking at Redis, as it's a very popular and useful key-value store.

### Pull the Redis image from Dockerhub (default repository for images)
```bash
# Pull the open-source image, the syntax is 'image_name:image_tag' where 'latest' is the default 'image_tag'.
$ docker pull redis

Using default tag: latest
latest: Pulling from library/redis
Digest: sha256:7e2c6181ad5c425443b56c7c73a9cd6df24a122345847d1ea9bb86a5afc76325
Status: Image is up to date for redis:latest
docker.io/library/redis:latest
```

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

```bash
$ docker rm redis

redis
```

### Recreate and see that the data doesn't exist anymore

```bash
$ docker run --rm --name redis -d redis:latest && docker exec -it redis redis-cli GET myname; docker stop redis;

(nil)
```

## Using Docker Volumes to preserve container data

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

Let's create a container to utilize the code in `python-app/redis_client.py`. Our image is going to look very similar to the one we viewed earlier.

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

### Build our image

```bash
# Build our container and tag (name) it as "bootcamp". The `python-app` tells docker what context to use for building the image. In this case we want to be inside of the folder that has our code.
$ docker build -f python-app/Dockerfile -t bootcamp python-app
```
Let's run our code without arguments to see what it can do

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

Alright! Let's just make sure we can connect to Redis with `check_redis`.

```bash
$ docker run bootcamp check_redis

...
  File "/usr/local/lib/python3.8/site-packages/redis/connection.py", line 1192, in get_connection
    connection.connect()
  File "/usr/local/lib/python3.8/site-packages/redis/connection.py", line 563, in connect
    raise ConnectionError(self._error_message(e))
redis.exceptions.ConnectionError: Error -2 connecting to redis:6379. Name or service not known.
```

What's going on? Well remember how everything is isolated, this is actually a good thing. You need to explicitly tell docker that these containers can communicate with eachother. To do this, we need to create a Docker Network.

## Connect Docker Containers

Create a docker network to act as an network environment for multiple containers.

```bash
$ docker network create bootcamp_net --attachable

<id>
```

Okay now that we have a network, let's attach our redis container to it.

```bash
$ docker network connect bootcamp_net redis --alias redis

...
```

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

That's what we're looking for. Okay cool, now we need to run our container with this network as well.

```bash
$ docker run --net bootcamp_net bootcamp check_redis

True
```

Yay! Now we can connect to redis from our other container. Let's check on that data from earlier:

```bash
$ docker run -t --net  bootcamp_net bootcamp get_data myname

The data is in redis!
key='myname'
val='Andrew'
```

We can also store new data using an interactive shell (`-i`):

```bash
$ docker run -it --net  bootcamp_net bootcamp store_data

What should we call this data?
thebestfood
What is the data?
potato
The data has been stored in redis
 ```

Now let's check for that new data:

```bash
$ docker run -t --net  bootcamp_net bootcamp get_data thebestfood

The data is in redis!
key='thebestfood'
val='potato'
```

Hopefully through this exercise you can see that docker can unlock some amazing development power, while remaining a secure platform to build and run containers from.

## Speeding things up with Docker Compose

So far it's kind of been a nightmare of cli commands. There has to be a better way right...?

TODO: Last part