from tornado.web import RequestHandler
import json

class MainPageHandler(RequestHandler):
    async def get(self):
        self.write(json.dumps({
            'available_urls': [
                {'method': 'POST', 'url': '/api/send_data', 'json_body': True}, 
            ]
        },
        indent=4
        ))