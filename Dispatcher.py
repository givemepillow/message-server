import json
from json import JSONDecodeError

from Clients import Clients
from DataTypes import Type
from Handlers import Handlers


class Dispatcher:
    __handlers = {
        Type.MESSAGE: Handlers.send_message,
        Type.DELETE_DIALOG: Handlers.delete_dialog,
        Type.DELETE_MASSAGE: Handlers.delete_message,
        Type.ERROR: Handlers.error
    }

    @classmethod
    def handle(cls, data, fd):
        try:
            request = cls.__load_request(data)
            user_id = cls.__extract_user_id(request, fd)
            answer = cls.__execute_handler(request)
            return user_id, answer
        except ValueError as e:
            _ERROR = -1
            return _ERROR, cls.__error_handler(str(e))

    @classmethod
    def __error_handler(cls, error_message):
        _answer = cls.__handlers[Type.ERROR](error_message)
        return json.dumps(_answer).encode('utf-8')

    @classmethod
    def __execute_handler(cls, request):
        try:
            _answer = cls.__handlers[request['type']](request)
            return json.dumps(_answer).encode('utf-8')
        except KeyError:
            raise ValueError("Invalid request type.")

    @classmethod
    def __extract_user_id(cls, request, fd):
        try:
            _user_id = int(request['from_id'])
            Clients.set_client(_user_id, fd)
        except KeyError:
            raise ValueError("Invalid data structure.")

    @classmethod
    def __load_request(cls, data):
        try:
            return json.loads(data.decode('utf-8'))
        except JSONDecodeError:
            raise ValueError("Invalid data.")
