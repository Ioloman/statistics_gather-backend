import os
from databases import Database
from tornado.ioloop import IOLoop
import tornado.web
from tornado.httpserver import HTTPServer
from app.receive_handler import ReceiveHandler
from app.main_handler import MainPageHandler
from dotenv import load_dotenv



def make_app(database: Database):
    # pass connection to each handler
    return tornado.web.Application([
        tornado.web.url(
            r'/', tornado.web.RedirectHandler, {'url': '/api'}
        ),
        tornado.web.url(
            r'/api', MainPageHandler, name='main'
        ),
        tornado.web.url(
            r'/api/send_data', ReceiveHandler, {'connection': database.connection()}, name='send_data'
        )
    ])


def main():
    # create database object and connect
    mysql_url = os.getenv('DATABASE_URL')
    print(mysql_url)
    database = Database(mysql_url)
    IOLoop.current().run_sync(lambda: database.connect())
    # create app and run server
    app = make_app(database)
    server = HTTPServer(app)
    server.listen(os.getenv('APP_PORT'), address=os.getenv('APP_HOST'))
    print(f"The server is up and running at {os.getenv('APP_HOST')}:{os.getenv('APP_PORT')}")
    IOLoop.current().start()


if __name__ == '__main__':
    load_dotenv('.env')
    main()
