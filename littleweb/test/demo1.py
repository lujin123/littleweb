import logging

from littleweb.test import web_copy


def index(req, resp):
    yield from resp.awrite("HTTP/1.0 200 OK\r\n")
    yield from resp.awrite("Content-Type: text/html\r\n")
    yield from resp.awrite("\r\n")
    yield from resp.awrite("I can show you a table of <a href='squares'>squares</a>.")


ROUTES = [
    ("/", index)
]

logging.basicConfig(level=logging.INFO)
app = web_copy.Application(ROUTES)
app.run(debug=True)
