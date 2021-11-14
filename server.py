import selectors
import socket
from Dispatcher import Dispatcher
from Clients import Clients


class Server:
    __selector = selectors.DefaultSelector()
    __BUFFER_SIZE = 1024 * 10
    __BACKLOG = 100
    __PORT = 6700
    __ADDRESS = '127.0.0.1'

    @classmethod
    def __init(cls):
        sock = socket.socket()
        sock.bind((cls.__ADDRESS, cls.__PORT))
        sock.listen(cls.__BACKLOG)
        sock.setblocking(False)
        cls.__selector.register(sock, selectors.EVENT_READ, cls.accept)

    @classmethod
    def start(cls):
        cls.__init()
        while True:
            events = cls.__selector.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)

    @classmethod
    def accept(cls, sock, mask):
        connection, addr = sock.accept()  # Should be ready
        print('accepted', connection, 'from', addr)
        Clients.set_connection(connection, connection.fileno())  # save client socket
        connection.setblocking(False)
        cls.__selector.register(connection, selectors.EVENT_READ, cls.read)

    @classmethod
    def read(cls, connection, mask):
        try:
            data = connection.recv(cls.__BUFFER_SIZE)  # Should be ready
            if data:
                print('rec: ', repr(data), 'to', connection)
                receiver, answer_data = Dispatcher.handle(data, connection.fileno())
                for user_fd in Clients.get_user(receiver):
                    Clients.connections[user_fd].send(answer_data)
                connection.send(answer_data)
            else:
                print('closing', connection)
                cls.close(connection)
        except OSError as err:
            print(err)
            cls.close(connection)

    @classmethod
    def close(cls, connection):
        Clients.remove_connection(connection.fileno())
        connection.close()
        cls.__selector.unregister(connection)
