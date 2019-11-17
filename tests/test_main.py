# -*- coding: utf-8 -*-
from . import client


def test_home():
    response = client.get("/")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}
