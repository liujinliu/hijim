# -*- coding: utf-8 -*-
import pytest


@pytest.mark.gen_test
async def test_app_create(client):
    url = '/api/v1/app'
    data = dict(name='demo_app')
    res = await client.fetch(uri=url, method='POST', json_data=data)
    assert res.code == 200
