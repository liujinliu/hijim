# -*- coding: utf-8 -*-
import pytest
from hijim.model.app import App
from .helper import get_mod_by_id, delete_app_by_name


@pytest.mark.gen_test
async def test_app_create(client):
    await delete_app_by_name('demo_app')
    url = '/api/v1/app'
    data = dict(name='demo_app')
    res = await client.fetch(uri=url, method='POST', json_data=data)
    assert res.code == 200
    assert res.json_data['id'] > 0
    app_id = res.json_data['id']
    app = await get_mod_by_id(App, app_id)
    assert app.name == 'demo_app'
    assert app.author == 'liujinliu'
    url = f'/api/v1/app/{app_id}'
    resp = await client.fetch(url)
    assert resp.code == 200
    assert resp.json_data['config']['info']['name'] == 'demo_app'

