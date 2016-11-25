import asyncio
from asyncio import coroutine


class Application(object):
    def __init__(self, routes=None):
        if routes:
            self.url_maps = routes
        else:
            self.url_maps = []

    @coroutine
    def handle(self, reader, writer):
        request_line = yield from reader.readline()
        print('request_line: ', request_line)
        if request_line == b'':
            writer.close()
            return

        method, path, proto = request_line.split()
        print('method={0},path={1},proto={2}'.format(method, path, proto))

        data = b''
        while 1:
            buffer = yield from reader.read(8)
            if not buffer:
                break
            data += buffer
            print('data: ', data)

        headers = {}
        while 1:
            line = yield from reader.readline()
            print('line: ', line)
            if line == b'\r\n':
                break
            line = line.decode()
            k, v = line.split(':', 1)
            headers[k] = v.rstrip()
        print('headers: ', headers)

        # todo 需要根据请求头的content-length来判断是否需要读取body中的数据，否则如果没有数据还去读取就会没有响应
        # data = yield from reader.read(1024)
        # print('data: ', data)
        # message = data.decode() or "hello world!"
        message = 'hello world...'
        addr = writer.get_extra_info('peername')
        print("Received %r from %r" % (message, addr))

        print("Send: %r" % message)
        writer.write(message.encode())
        yield from writer.drain()

        print("Close the client socket")
        writer.close()
        print('=================================================')

    def run(self, host='127.0.0.1', port=8080, debug=True):
        if debug:
            print("* Running on http://%s:%s/" % (host, port))
        loop = asyncio.get_event_loop()
        coro = asyncio.start_server(self.handle, host, port, loop=loop)
        server = loop.run_until_complete(coro)

        # Serve requests until Ctrl+C is pressed
        print('Serving on {}'.format(server.sockets[0].getsockname()))
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass

        # Close the server
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()
