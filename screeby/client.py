import json
import logging
from screeby.remote_video import RemoteVideoConnection
from screeby.network import sock

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

    def recv_response(self, message, decode=True):
        with sock(self.server_addr()) as s:
            s.send(message.encode())
            message = s.recv(8192)

        if not message:
            return None

        if decode:
            return message.decode()

        return message
