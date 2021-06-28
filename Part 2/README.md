# 2021 Bootcamp CI/CD & Docker (pt. 2)

In Part 1, you learned about:

- Docker Images
- Docker Commands
- Docker-Compose

In this session, we are going to expand on the concept of using docker-compose to build really powerful environments.

## The Power of Docker

### docker-compose refresher

Docker-compose makes it super easy to get started with open-source software. Since it's a standardized and versioned format, you can be sure that it'll work the same across environments and ecosystems. In their words:

>> Compose is a tool for defining and running multi-container Docker applications. With Compose, you use a YAML file to configure your application’s services. Then, with a single command, you create and start all the services from your configuration. 



## Advanced Docker Compose Example

### Step 1: Create Django Project

> In this example, we are going to use the end result of the `Writing your first Django app` tutorial on their [website](https://docs.djangoproject.com/en/3.2/intro/). Don't worry, you won't have to go through the tutorial yourself, but it's important to know where this code is coming from. All this example does is provide an example Polls application written in Django. If you aren't familiar, Django is a python framework for developing dynamic and modern websites. For this tutorial, you won't need to be a Django expert, just realize that it's creating a website for you when we run our first docker-compose.

Here's what the first [docker-compose.yml](Django/docker-compose.yml) looks like:

```yaml
version: "3.9"
   
services:
  db:
    image: postgres
    volumes:
      - ./data/db:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
  web:
    build: .
    volumes:
      - .:/code
    environment:
      ELASTIC_APM_ENABLED: "false"
      ELASTIC_APM_SERVICE_NAME: bootcamp-django
    ports:
      - "8000:8000"
    depends_on:
      - db
```

The first service created is the postgress database. This allows our Django site to store and maintain it's application state. In this example, we simply use a local directory (via `volumes`) for it's database storage, and you'll see that created automatically for you by compose. We also pass through some environment variables which represent how we connect to the postgress database from Django.

 The second service is our [Django application](Django/). We use the `volumes` declaration to mount our Django code into the container. This allows us to make changes to the website code files, and have them reflected immediately via Django's autoreload mechanism.

#### Deploy Django Service

```bash
$ cd Part\ 2/Django/
$ docker-compose up -d


...
Starting django_db_1 ... done
Starting django_web_1 ... done
```

Congrats! Your website should now be running at http://0.0.0.0:8000. The admin endpoint is running at: http://0.0.0.0:8000/admin/. The credentials for the admin endpoint are:

```yml
Username: admin
Password: bootcamp
```

#### Exec into Django

Using docker-compose commands, we are able to access the Django Command Line Interface (CLI) in order to run useful commands. For example, let's use the CLI to create a poll for our website.

```bash
$ docker-compose exec web python manage.py shell

DEBUG=True
Python 3.9.5 (default, Jun 23 2021, 15:01:51) 
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> 
```

We are now in the interactive Python shell for Django! We are able to run a lot of useful commands here, such as flushing the database, creating superusers, modifying database objects, and more.

Let's import the code we need:
```python
>>> from djangobootcamp.polls.models import Choice, Question
>>> from django.utils import timezone
```

Then let's list our polls:
```python
>>> Question.objects.all()

<QuerySet []>
```

So we don't have any polls so far, this is expected. Let's create one!

#### Create a Poll

```python
>>> question_text = "Which is best, tabs or spaces?"
>>> q = Question.objects.create(question_text=question_text, pub_date=timezone.now())

<Question: Which is best, tabs or spaces?>
```

Save the question to the database.

```python
>>> q.save()
>>> q.id  # We now have an id!
```

Check the possible answers to the question:

```python
>>> q.choice_set.all()

<QuerySet []>
```

#### Create some answers

We don't have any possible answers yet, so let's create some:

```python
>>> q.choice_set.create(choice_text='Tabs', votes=0).save()
>>> q.choice_set.create(choice_text='Spaces', votes=0).save()
>>> q.choice_set.create(choice_text='But why does it matter?', votes=0).save()
```

Ok now we have some possible answers, let's make sure they exist:

```python
>>> q.choice_set.all()

<QuerySet [<Choice: Tabs>, <Choice: Spaces>, <Choice: But why does it matter?>]>
```

Perfect, I think we're ready to accept some answers at the site [URL](http://localhost:8000).

#### Exit the shell

```python
>>> exit()
```

#### Recap

With just a few lines, we were able to create a fully functional website, using commands from inside of the container. Are you a docker believer yet?

### Step 2: Deploy the Elastic Stack

> Now that we have a website running, it's very important to include some monitoring around it so that we can validate that things are working as we expect. For this section, we are going to deploy the popular [Elastic stack](elastic.co) so that we can use their powerful tools to check on our site.

#### What is the Elastic Stack?

At a high level, the Elastic stack contains a bunch of different applications that help developers monitor and track their programs. In this session, we will deploy the following tools from the Elastic Stack:

##### Elasticsearch


Elasticsearch is an indexing application that allows you to search through large datasets. It is the foundation for all of the other components of the Elastic Stack.

##### Kibana

Kibana is the UI frontend into Elasticsearch. It's extremely powerful in terms of building visualizations and dashboards around your data. Most people rarely interact with Elasticsearch directly - Rather, they use Kibana as a middle-man to see the data they are looking for.

##### Elastic-APM
Elastic APM is a service that allows you to instrument and monitor the performance of your code. Using Elastic APM, you are able to see detailed insights into the minor details of the performance of your code. This tool is a must-have for production apps on my team.

##### Filebeat

Filebeat is a log shipper. The purpose of it is to feed data into Elasticsearch from various sources. In this example, it's included to ship your local Docker logs into Elasticsearch.
#### Deploy the Elastic Stack

```bash
$ cd ../ELK
$ docker-compose up -d  # This might take a while...

...
Creating es ... done
Creating filebeat         ... done
Creating elk_apm-server_1 ... done
Creating kib              ... done
```

After running that command, you will have a multitude of services avaiable to you. You can always check them with `docker-compose ps`.


```bash
$ docker-compose ps


      Name                    Command                       State                                                 Ports                                       
--------------------------------------------------------------------------------------------------------------------------------------------------------------
elk_apm-server_1   /usr/local/bin/docker-entr ...   Up (healthy)            127.0.0.1:6060->6060/tcp, 127.0.0.1:8200->8200/tcp                                
es                 /tini -- /usr/local/bin/do ...   Up (healthy)            0.0.0.0:9200->9200/tcp,:::9200->9200/tcp, 0.0.0.0:9300->9300/tcp,:::9300->9300/tcp
filebeat           /usr/local/bin/docker-entr ...   Up                                                                                                        
kib                /usr/local/bin/dumb-init - ...   Up (health: starting)   0.0.0.0:5601->5601/tcp,:::5601->5601/tcp
```

> See how the above logs show `healthy` for some of the services? That's beacuse these services have a `HEALTHCHECK` defined. This allows you to make sure that the individual containers in your services are working as you expect.

##### Use the Elastic Stack

You should now see your application logs from Django when you visit: http://localhost:5601/app/logs/

When you perform actions on the website, such as going to a new page, you'll see those actions reflected in the logs in Kibana.

This is pretty cool, but what else can we do with Kibana?

##### 

### Step 3: 

```bash
$ 



```

### Docker-Compose Overrides

### Clean Development Environments using Docker

### Monitoring using Docker

## 