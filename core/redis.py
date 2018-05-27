import redis
from os import environ

REDIS_CACHE = redis.StrictRedis(
    environ.get('REDIS_HOST', 'redis-10097.c16.us-east-1-3.ec2.cloud.redislabs.com'),
    port=environ.get('REDIS_PORT', '10097'),
    db=environ.get('REDIS_DB', 0),
    password=environ.get('REDIS_PASSWORD', 'ijnTpDaZ4E5TP0Lr4RK6Whw4IhH22Mhu')
)
