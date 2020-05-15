import json
import logging
from screeby.remote_video import RemoteVideoConnection
from screeby.network import response

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
        message = response(self.server_addr(), 'SERVER_INFO')
        if not message:
            return None

        client_logger.info(f"{self.server_addr()} : Got server info: {message}")
        return json.loads(message)

