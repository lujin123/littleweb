import asyncio
import json
import re

from littleweb import utils
from littleweb.server import ServerHttpProtocol


class Application(object):
    def __init__(self, router=None):
        self._router = router or []

    def route(self, url):
        def _decorate(cls):
            self.add_router(url, cls)
            return cls

        return _decorate

    def add_router(self, url, cls):
        self._router.append((url, cls))

    def add_router_batch(self, routes):
        self._router += routes

    def make_handler(self):
        self._router = self.format_url(self._router)
        return ServerHttpProtocol(self._router)

    @staticmethod
    def format_url(router):
        routers = []
        for pattern, cls in router:
            if not pattern.startswith('^'):
                pattern = r'^' + pattern
            if not pattern.endswith('$'):
                pattern += r'$'
            routers.append((re.compile(pattern), cls))
        return routers

    def run(self, host='127.0.0.1', port=8080, debug=True):
        loop = asyncio.get_event_loop()
        coro = loop.create_server(self.make_handler, host, port)
        server = loop.run_until_complete(coro)
        print('* Serving on {}'.format(server.sockets[0].getsockname()))
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()


class BaseHandler(object):
    def __init__(self):
        self.request = None
        self.response = None

    def get_query_int(self, key, default=None, min_value=None, max_value=None):
        res = self.get_query_str(key, default)
        value = utils.str2int(res, default)
        if min_value is not None:
            value = max(value, min_value)
        if max_value is not None:
            value = min(value, max_value)
        return value

    def get_query_bool(self, key, default=False):
        res = self.get_query_str(key)
        return utils.str2bool(res, default)

    def get_query_json(self, key, default=None):
        res = self.get_query_str(key, default)
        return utils.str2json(res, default)

    def get_query_str(self, key, default=None):
        query_params = self.get_request_data('query_params', {})
        return query_params.get(key, default)

    def get_request_data(self, key, default=None):
        if self.request:
            return getattr(self.request, key, default)
        return default

    def get_post_str(self, key, default=None):
        body_params = self.get_request_data('body_params', {})
        return body_params.get(key, default)

    def get_post_int(self, key, default=None, min_value=None, max_value=None):
        res = self.get_post_str(key, default)
        value = utils.str2int(res, default)
        if min_value is not None:
            value = max(value, min_value)
        if max_value is not None:
            value = min(value, max_value)
        return value

    def get_post_bool(self, key, default=False):
        res = self.get_post_str(key)
        return utils.str2bool(res, default)

    def get_post_json(self, key, default=None):
        res = self.get_post_str(key, default)
        return utils.str2json(res, default)

    def send_data(self, data, status_code=200):
        self.response.status_code = status_code
        self.response.send_data(data)

    def send_json(self, data, status_code=200):
        data = json.dumps(data)
        self.response.add_header('Content-Type', 'application/json')
        self.send_data(data, status_code)
