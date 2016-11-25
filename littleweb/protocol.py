__all__ = ["HttpParser"]


class HttpParser(object):
    def __init__(self, data, max_headers=32768, max_field_size=8190):
        self._data = data
        self.max_headers = max_headers
        self.max_field_size = max_field_size
        self.headers = {}
        self.body_params = {}
        self.query_params = {}
        self.method = 'GET'
        self.path = '/',
        self.protocol = 'HTTP/1.1'
        self.resource = '/'

    def parse_data(self):
        data = self._data.decode()
        header, body = data.split('\r\n\r\n')
        rows = header.split('\r\n')
        line = rows[0]
        row_headers = rows[1:]

        self.method, self.path, self.protocol = HttpParser.parse_request_line(line)
        self.resource, self.query_params = HttpParser.parse_query(self.path)
        self.headers = HttpParser.parse_headers(row_headers)
        self.body_params = HttpParser.parse_body(body)

    @staticmethod
    def parse_request_line(line):
        return line.split(" ")

    @staticmethod
    def parse_query(path):
        resource, query_str = path.split('?', 1) if '?' in path else (path, None)
        query_params = {}
        if query_str:
            query, anchor = query_str.split('#', 1) if '#' in query_str else (query_str, None)
            row_params = query.split('&', 1)
            for param in row_params:
                key, value = param.split('=', 1)
                if key:
                    query_params[key] = value

        return resource, query_params

    @staticmethod
    def parse_headers(row_headers):
        # todo 检查header是否合法
        headers = {}
        for header in row_headers:
            key, value = header.split(':', 1)
            headers[key.lower()] = value.strip()
        return headers

    @staticmethod
    def parse_body(body):
        body_params = {}
        if not body:
            return body_params

        bodies = body.split('&', 1)
        for b in bodies:
            key, value = b.split('=', 1)
            if key:
                body_params[key] = value

        return body_params

    def check_headers(self):
        pass
