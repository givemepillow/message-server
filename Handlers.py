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
        request['messages'] = storage.get_messages(
            last_message_id=request['last_message_id'],
            target_id=request['from_id']
        )
        return request

    @staticmethod
    def send_message(request):
        _from_id = request['from_id']
        _to_id = request['to_id']
        request['date_time'] = datetime.now().timestamp() * 1000
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
        storage.delete_dialog(
            user1_id=_from_id,
            user2_id=_to_id
        )
        return request

