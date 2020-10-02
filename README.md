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

* Convert an ESRI shapefile to GEOJSON
* Make a geocode request
* Convert coordinates from one projection to another

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