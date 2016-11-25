import asyncio
from asyncio import coroutine

from littleweb.web import Application, BaseHandler


class Index(BaseHandler):
    @coroutine
    def get(self, id, name='sss'):
        print('request:', self.request.headers)
        print('id: ', id)
        print('name: ', name)
        print('index get method...')
        yield from asyncio.sleep(1)
        print('yield after')
        res = {
            'id': id,
            'name': name
        }
        self.send_json(res, 201)


routes = [
    (r'/index/(?P<id>\d+)/(\w+)', Index)
]

app = Application(routes)
app.run(port=8888)
