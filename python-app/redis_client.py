import fire
from redis import Redis
import os

REDIS_HOST = os.environ.get("REDIS_HOST", "redis")

data = {}


def store_data():
    key = input("What should we call this data?\n")
    value = input("What is the data?\n")

    c = get_redis_client()
    c.set(key, value)
    print("The data has been stored in redis")


def get_data(key=None, *a, **k):
    key = key or input("What was name of the data?\n")
    val = None
    if key:
        c = get_redis_client()
        val = c.get(key)
        if val:
            print("The data is in redis!")
            val = val.decode()
        else:
            val = "Not Found"
    return f"{key=}\n{val=}"


def get_redis_client():
    redis_client = Redis(host=REDIS_HOST)
    return redis_client


def hello_world():
    print("Oh hai")


def check_redis():
    c = get_redis_client()
    if c:
        c.set(name="test", value="test")
        c.get("test")
        c.delete("test")
        print("True")
        exit(0)
    
    exit(1)


if __name__ == '__main__':
    fire.Fire(dict(
        store_data=store_data,
        get_data=get_data,
        check_redis=check_redis,
        hello_world=hello_world
    ))
