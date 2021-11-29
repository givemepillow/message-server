from datetime import datetime

from DataTypes import Type

from loader import storage


class Handlers:
    @staticmethod
    def error(info):
        return {
            'type': Type.ERROR,
            'error': info
        }

    @staticmethod
    def init(request):
        return request

    @staticmethod
    def send_message(request):
        _from_id = request['from_id']
        _to_id = request['to_id']
        request['date_time'] = datetime.now().timestamp() * 1000
        print(request['date_time'])
        _message = request['message']
        # save message to db
        request['message_id'] = storage.save_message(
            request['from_id'],
            request['to_id'],
            request['date_time'],
            request['message']
        )
        return request

    @staticmethod
    def delete_message(request):
        _from_id = request['from_id']
        _to_id = request['to_id']
        _message_id = request['message_id']
        # delete message from db
        return request

    @staticmethod
    def delete_dialog(request):
        _from_id = request['from_id']
        _to_id = request['to_id']
        # delete message history from db (for all)
        return request
