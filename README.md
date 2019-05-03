Mongo Sharded Cluster Monitoring with Django and Docker Compose
=========================================

A simple sharded Mongo Cluster monitoring application using with Django and Docker to test replica set health.

It is designed to monitor and experimental purpose to investigate replica set behaviours during `polling` and under massive request.
Django is used to virtualise the data on the backend. Moreover, Vue JS is used for frontend with Apexcharts.

![screenshot](https://github.com/omegion/Mongo-Sharded-Cluster-Monitoring-with-Django-and-Docker-Compose/blob/master/screenshot.png?raw=true "Screenshot")


### Mongo Components

* Config Server (3 member replica set): `config01`,`config02`,`config03`
* 1 Shard (with 3 members replica set):
	* `shard01a`,`shard01b`, `shard01c`
* 1 Router (mongos): `router`

### Docker Containers
This system uses Docker container to create an virtual environment to test our cluster. FOr this purpose we have defined resources to replica container.
The container has 20% of total CPU and 200MB of memory of the host.

### First Run (initial setup)
**Start all of the containers** (daemonized)

```
docker-compose up -d
```

**Initialize the replica sets (config server and shards) and router**

```
sh init.sh
```

This script has a `sleep 20` to wait for the config server and shards to elect their primaries before initializing the router

### Accessing the Mongo Shell
Its as simple as:

```
docker-compose exec router mongo
```

### Resetting the Cluster
To remove all data and re-initialize the cluster, make sure the containers are stopped and then:

```
docker-compose rm
```

Execute the **First Run** instructions again.


Inspired by [https://github.com/chefsplate/mongo-shard-docker-compose](https://github.com/chefsplate/mongo-shard-docker-compose)
