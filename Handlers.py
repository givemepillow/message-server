from datetime import datetime

from DataTypes import Type


class Handlers:
    @staticmethod
    def error(info):
        return {
            'type': Type.ERROR,
            'error': info
        }

    @staticmethod
    def send_message(request):
        _from_id = request['from_id']
        _to_id = request['to_id']
        request['date_time'] = datetime.now().strftime("%m-%d-%Y, %H:%M:%S")
        _message = request['message']
        # save message to db
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
