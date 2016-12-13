# littleweb
asyncio framework

## use
server code:

```python
import asyncio
from asyncio import coroutine

from littleweb.web import Application, BaseHandler


class Index(BaseHandler):
    @coroutine
    def get(self, id, name='sss'):
        yield from asyncio.sleep(1)
        res = {
            'id': id,
            'name': name
        }
        self.send_json(res, 200)

routes = [
    (r'/index/(?P<id>\d+)/(\w+)', Index)
]

app = Application(routes)
app.run()

```

also can use decorator:

```python
from asyncio import coroutine

from littleweb.web import Application, BaseHandler

app = Application()


@app.route('/index/(?P<id>\d+)/(\w+)')
class Index(BaseHandler):
    @coroutine
    def get(self, id, name='sss'):
        print('id: ', id)
        print('name: ', name)
        res = {
            'id': id,
            'name': name
        }
        return self.send_json(res)

app.run(port=8888)

```




test code:

```python
import threading

import requests


def test(i):
    print('thread ==> ', i)
    resp = requests.get('http://localhost:8080/index/' + str(i) + '/hello')
    print(resp.content)


def main():
    thread_pool = []

    for i in range(10):
        th = threading.Thread(target=test, args=(i,))
        thread_pool.append(th)

    for th in thread_pool:
        th.start()

    for th in thread_pool:
        threading.Thread.join(th)


if __name__ == '__main__':
    main()

```

## todo list

1. database
2. ~~flask style url (use decorator)~~
3. log
4. middleware