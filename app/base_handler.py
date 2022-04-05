from tornado.web import RequestHandler
from databases.core import Connection
import json


class BaseHandler(RequestHandler):
    """
    base class for handlers
    """

    def initialize(self, connection: Connection):
        self.connection = connection

    # override error page
    def write_error(self, status_code: int, **kwargs) -> None:
        self.finish(json.dumps({
            'error': f'{status_code} {self._reason}'
        }))

    # set header
    def prepare(self):
        self.set_header('Content-Type', 'application/json')