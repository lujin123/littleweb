import asyncio
import inspect
import re

from littleweb.protocol import HttpParser


class ServerHttpProtocol(asyncio.Protocol):
    def __init__(self, router=None):
        self._routers = router or []
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def connection_lost(self, exc):
        self.transport = None

    def data_received(self, data):
        asyncio.ensure_future(self.process_data(data))

    @asyncio.coroutine
    def process_data(self, data):
        request = HttpRequest(data)
        response = HttpResponse(self.transport, {})

        for pattern, cls in self._routers:
            m = re.match(pattern, request.resource)
            if m:
                args = m.groups()
                method = request.method.lower()
                if hasattr(cls, method):
                    fn = getattr(cls, method)
                    if fn and callable(fn):
                        if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
                            fn = asyncio.coroutine(fn)
                        instance = cls()
                        instance.request = request
                        instance.response = response

                        # todo 调用之前可以进行一些操作 middleware
                        yield from fn(instance, *args)
                        return

        self.handle_404(response)

    @staticmethod
    def handle_404(response):
        response.add_header('Content-Type', 'text/html')
        response.send_data('Page Not Found!')


class HttpResponse(object):
    def __init__(self, transport, headers=None, status_code=404):
        self._transport = transport
        self._headers = headers or {}
        self._version = [1, 1]
        self._status_code = status_code

    def add_header(self, key, value):
        self._headers[key] = value

    @property
    def headers(self):
        return self._headers

    @property
    def status_code(self):
        return self._status_code

    @status_code.setter
    def status_code(self, code):
        self._status_code = code

    def write_data(self, data):
        self._transport.write(data.encode())

    def write_eof(self):
        self._transport.close()

    def send_data(self, data):
        self.add_header('Content-Length', len(data))
        self.send_headers()
        self.write_data(data)
        self.write_eof()

    def status_line(self):
        # todo http状态码和描述的映射关系
        return 'HTTP/%s.%s %s %s\r\n' % (self._version[0], self._version[1], self._status_code, 'OK')

    def send_headers(self, sep=': ', end='\r\n'):
        headers = self.status_line() + ''.join([str(k) + sep + str(v) + end for k, v in self._headers.items()]) + '\r\n'
        self.write_data(headers)


class HttpRequest(HttpParser):
    def __init__(self, data):
        super().__init__(data)
        self.parse_data()
