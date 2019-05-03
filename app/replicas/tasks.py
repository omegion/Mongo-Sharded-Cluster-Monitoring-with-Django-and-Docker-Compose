import os
import time
import subprocess
import logging
from django.conf import settings
from django.utils import timezone
import datetime

# Models
from replicas.models import Replica, Check

# Get an instance of a logger  
logger = logging.getLogger(__name__)


from mongoengine import connect
import pymongo
from pymongo import MongoClient
import docker
from celery.decorators import task, periodic_task

# Regular connect

class Mongo(object):
    def __init__(self):
        self.conn = MongoClient('router', 27017)
        self.database = self.conn["test"]

    @property
    def db(self):
        return self.database

    @property
    def connection(self):
        return self.conn

@task(soft_time_limit=2700, bind=True)
def container_stats(*args, **karg):
    name = karg['name']
    replica = Replica.objects.filter(name=name).first()

    # connect to docker container
    client = docker.from_env()
    container = client.containers.get(name)
    stats = container.stats(stream=False)
    if stats:
        cpuDelta = stats['cpu_stats']['cpu_usage']['total_usage'] -  stats['precpu_stats']['cpu_usage']['total_usage']
        systemDelta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
        cpu_usage = cpuDelta / systemDelta * 100 * 5 # container can use only 20% of CPU
        mem_usage = (stats['memory_stats']['usage'] - stats['memory_stats']['stats']['active_file']) / stats['memory_stats']['limit'] * 100
        read = stats['blkio_stats']['io_service_bytes_recursive'][0]['value']

    # check if replica checks exceeds
    if replica.checks.count() > 100 and replica.checks.count() % 20 == 0:
        for check in replica.checks.order_by('-id')[100:]:
            check.delete()
    
    replica.checks.create(
        cpu=round(cpu_usage, 4),
        memory=round(mem_usage, 4),
        io=round(read, 4),
    )

@task(soft_time_limit=2700, bind=True)
def check_container_status(*args, **karg):
    shard = karg['shard']
    replicas = Replica.objects.filter(shard=shard).all()
    for replica in replicas:
        container_stats.apply_async(
            kwargs={'name': replica.name},
            countdown=0, # 1 sec
            expires=2700, # 45 mins
            queue='default',
        )

@task(soft_time_limit=2700, bind=True)
def update_replica_set(*args, **karg):
    shard = karg['shard']
    conn = MongoClient(shard+'a', 27018)
    db = conn.admin
    db_stats = db.command({'replSetGetStatus'  :1})
    for key in db_stats['members'] : 
        replica_name = key['name'].split(':')[0]
        state = key['stateStr']
        health = key['health']
        replica = Replica.objects.filter(name=replica_name).first()
        if replica:
            replica.state = state
            replica.health = health
            replica.save()

def replica_down(replica_name):
    conn = MongoClient(replica_name, 27018)
    db = conn.admin
    try:
        db.command({'replSetStepDown':1, 'force': True})
    except:
        pass

@task(soft_time_limit=2700, bind=True)
def start_reading_from_replica(*args, **karg):
    query = karg['query']
    # {"location" : "US", "factoryId" : {"$gte" : 1500}}

    # start to read from replica set around 20 seconds
    conn = MongoClient('router', 27017)
    db = conn.test
    # for i in range(10):
    return db.customers.find(query).count()

@task(soft_time_limit=2700, bind=True)
def insert_data_to_replica_set(*args, **karg):
    number = karg['number']
    # start to read from replica set around 20 seconds
    conn = MongoClient('router', 27017)
    db = conn.test
    for i in range(int(number)):
        mydict = { "location": "US", "factoryId": i + 100000 }
        db.customers.insert_one(mydict)

def start_benchmark(replica_name, shard="shard01"):

    container_stats(name="shard01a")
    # insert_data_to_replica()
    # start_reading_from_replica()
    # update_replica_set(shard=shard)
    # get primary replica
    # primary = Replica.objects.filter(shard=shard, state="PRIMARY").first()
    # if primary:
    #     container_stats(name=primary.name)
    #     replica_down(primary.name)
    # update_replica_set(shard=shard)
    pass