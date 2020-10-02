# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages


setup(
    name="pygisapi",
    author="3sLab",
    description="API providing GIS tools and features",
    license="MIT",
    keywords="api, gis, geojson, shapefile",
    url="https://github.com/3slab/pygisapi",
    packages=find_packages(exclude=["*.test", "*.test.*", "test.*", "test"]),
    install_requires=('fiona', 'shapely', 'fastapi', 'geopy', 'pyproj'),
    extras_require={
        'test': ['pytest', 'flake8']
    }
)
