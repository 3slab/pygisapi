# PyGIS API

API to provide gis features to projects

[![Build Status](https://travis-ci.org/3slab/pygisapi.svg?branch=master)](https://travis-ci.org/3slab/pygisapi)

This is based on [FastAPI](https://fastapi.tiangolo.com/)

## Install

It uses [pipenv](https://realpython.com/pipenv-guide/)

```
make init
```

## Run

```
make run
```

Go to `http://localhost:8000/docs` to view OpenAPI documentation

## Features

| Environment Variable | Description | Default Value | Example |
|---|---|---|---|
| `REDIS_HOST` | Redis server address | *(not set → Redis disabled)* | `localhost`, `redis.example.com`, `10.0.0.5` |
| `REDIS_PORT` | Redis server port | `6379` (if `REDIS_HOST` is set) | `6379` |
| `REDIS_DB` | Redis database number (0 to 15 by default) | `0` (if `REDIS_HOST` is set) | `0`, `1`, `2` |

**Behavior depending on configuration**

| Configuration | Behavior |
|---|---|
| No variable set | Works **without Redis** (in-memory cache only, previous behavior) |
| `REDIS_HOST` set alone | Connects to Redis on `REDIS_HOST:6379`, database `0` |
| `REDIS_HOST` + `REDIS_PORT` set | Connects to Redis on the specified port, database `0` |
| `REDIS_HOST` + `REDIS_PORT` + `REDIS_DB` set | Full connection with specific database |
| `REDIS_HOST` set but Redis unreachable | ⚠️ depends on your implementation (silent fallback or error?) |


* Convert an ESRI shapefile to GEOJSON
* Make a geocode request
* Convert coordinates from one projection to another
* Calculate centroid of a geojson

## Docker

A docker image is available : [3slab/pygisapi](https://hub.docker.com/r/3slab/pygisapi)

## Deployment

```
pipenv lock -r > requirements.txt
docker build -t 3slab/pygisapi:<version> .
docker tag 3slab/pygisapi:<version> 3slab/pygisapi:latest
docker push 3slab/pygisapi:<version>
git tag -a <version>
git push --tags
```