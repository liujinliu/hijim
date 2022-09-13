# -*- coding: utf-8 -*-
import os
os.environ.setdefault('DB_CONN', "sqlite+aiosqlite:///unitestdb")

import urllib
import json
import pytest
from tornado.httpclient import AsyncHTTPClient, HTTPRequest


class _WrappedHTTPResponse:

    def __init__(self, response):
        self.response = response

    def __getattr__(self, item):
        return getattr(self.response, item)

    @property
    def json(self):
        return json.loads(self.response.body)

    @property
    def json_data(self):
        return self.json['data']


class _WrappedHTTPClient:

    def __init__(self, base_url):
        self.base_url = base_url
        self.http_client = AsyncHTTPClient()

    def close(self):
        self.http_client.close()

    async def fetch(self, uri, method='GET', headers: dict = None,
                    data: dict = None, json_data: dict = None, **kwargs):
        headers = headers or dict()
        if method == 'GET':
            body = None
        elif json_data:
            headers['Content-Type'] = 'application/json'
            body = json.dumps(json_data)
        else:
            if not data:
                data = dict()
            body = urllib.parse.urlencode(data) or ''
        request = HTTPRequest(url=self.base_url + uri,
                              method=method,
                              body=body,
                              headers=headers,
                              allow_nonstandard_methods=True,
                              **kwargs)
        res = await self.http_client.fetch(request, raise_error=False)
        return _WrappedHTTPResponse(res)


@pytest.fixture
def app():
    from hijim.bin.main import HijimServer
    server = HijimServer()
    server.init_app()
    return server.app


@pytest.fixture
def client(request, base_url, http_server):
    cli = _WrappedHTTPClient(base_url)
    request.addfinalizer(cli.close)
    return cli
