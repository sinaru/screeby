from socket import socket, AF_INET, SOCK_STREAM
import json
import logging
from contextlib import contextmanager

client_logger = logging.getLogger('screeby.Client')


class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def server_addr(self):
        return (self.ip, self.port)

    def run(self):
        self.server_info = self.server_info()

    def server_info(self):
        message = self.recv_response('SERVER_INFO')
        if not message:
            return None

        client_logger.info(f"{self.server_addr()} : Got server info: {message}")
        return json.loads(message)

    @contextmanager
    def connection(self):
        sock = socket(AF_INET, SOCK_STREAM)
        try:
            sock.connect(self.server_addr())
            client_logger.info(f"{self.server_addr()} : Connected")
            yield sock
        finally:
            sock.close()

    def recv_response(self, message, decode=True):
        with self.connection() as sock:
            sock.send(message.encode())
            message = sock.recv(8192)

        if not message:
            return None

        if decode:
            return message.decode()

        return message
