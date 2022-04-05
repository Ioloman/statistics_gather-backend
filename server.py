import os
from databases import Database
from tornado.ioloop import IOLoop
import tornado.web
from tornado.httpserver import HTTPServer



def make_app(database: Database):
    # pass connection to each handler
    return tornado.web.Application([

    ])


def main():
    # create database object and connect
    database = Database(os.getenv('DATABASE_URL'))
    IOLoop.current().run_sync(lambda: database.connect())
    # create app and run server
    app = make_app(database)
    server = HTTPServer(app)
    server.listen(os.getenv('APP_PORT'), address=os.getenv('APP_HOST'))
    print(f"The server is up and running at {os.getenv('APP_HOST')}:{os.getenv('APP_PORT')}")
    IOLoop.current().start()


if __name__ == '__main__':
    main()