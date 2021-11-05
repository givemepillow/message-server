import selectors
import socket


class Server:
    __selector = selectors.DefaultSelector()
    __BUFFER_SIZE = 1024 * 25
    __BACKLOG = 100
    __PORT = 6700
    __ADDRESS = '127.0.0.1'

    @classmethod
    def _init(cls):
        sock = socket.socket()
        sock.bind((cls.__ADDRESS, cls.__PORT))
        sock.listen(cls.__BACKLOG)
        sock.setblocking(False)
        cls.__selector.register(sock, selectors.EVENT_READ, cls.accept)

    @classmethod
    def start(cls):
        while True:
            events = cls.__selector.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)

    @classmethod
    def accept(cls, sock, mask):
        conn, addr = sock.accept()  # Should be ready
        print('accepted', conn, 'from', addr)
        conn.setblocking(False)
        cls.__selector.register(conn, selectors.EVENT_READ, cls.read)

    @classmethod
    def read(cls, connection, mask):
        data = connection.recv(cls.__BUFFER_SIZE)  # Should be ready
        if data:
            print('echoing', repr(data), 'to', connection)
            connection.send(data)  # Hope it won't block
        else:
            print('closing', connection)
            cls.__selector.unregister(connection)
            connection.close()
