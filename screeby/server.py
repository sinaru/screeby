import logging
from socketserver import BaseRequestHandler, TCPServer

server_logger = logging.getLogger('screeby.Server')


class ClientMessage:
    def __init__(self, message):
        self.message_parts = message.decode().split('|')
        self.message_type = self.message_parts[0]

    def type(self):
        return self.message_type


class ServerRequestHandler(BaseRequestHandler):
    def handle(self):
        server_logger.info(f"Connected with: {self.client_address}")
        msg = self.request.recv(8192)
        if not msg:
            server_logger.info(f"Connection closed with: {self.client_address}")

        msg = ClientMessage(msg)

        if msg.type() == 'SERVER_INFO':
            self.send_server_info()

    def send_server_info(self):
        self.send_str("RESOLUTION:1366x768")

    def send_str(self, text):
        self.request.send(text.encode())


class Server:
    def __init__(self, port):
        server_logger.info('listening to connections...')
        TCPServer.allow_reuse_address = True
        self.serve = TCPServer(('', port), ServerRequestHandler)

    def run(self):
        self.serve.serve_forever()
