from .base_handler import BaseHandler
from tornado.web import HTTPError
import json
from . import queries


def validate_json(json_: bytes) -> bool:
    """try to parse json and perform other checks to make sure it is valid

    Args:
        json_ (bytes): raw body with json
    """
    try:
        request = json.loads(json_)
    except json.JSONDecodeError:
        return False

    if not type(request) is dict:
        return False

    if not request.get('device_name') or type(request.get('time_series')) is not list:
        return False

    return True


class ReceiveHandler(BaseHandler):
    async def post(self):
        # validate json
        if not validate_json(self.request.body):
            raise HTTPError(400)

        # get data_source id
        data = json.loads(self.request.body)
        async with self.connection:
            if (source_id := await queries.get_data_source_id(self.connection, data['device_name'])) is None:
                source_id = await queries.add_data_source(self.connection, data['device_name'])
        # restructure data
        parsed_data = {}
        for frame in data['time_series']:
            for field, value in frame['stats'].items():
                if parsed_data.get(field) is None:
                    parsed_data[field] = []
                parsed_data[field].append({'value': value, 'date': frame['date']})

        # add data to the database
        async with self.connection:
            for field, records in parsed_data.items():
                # get field id
                if (field_id := await queries.get_field_id(self.connection, field, source_id)) is None:
                    field_id = await queries.add_field(self.connection, field, source_id)
                # insert data
                await queries.add_records(self.connection, field_id, records)

        self.write(json.dumps({'status': 'success'}))
