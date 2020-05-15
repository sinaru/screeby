import logging
from socketserver import BaseRequestHandler, TCPServer
import json
import subprocess
from time import sleep
from screeninfo import get_monitors

server_logger = logging.getLogger('screeby.Server')
network_logger = logging.getLogger('screeby.Network')


class ServerRequestHandler(BaseRequestHandler):
    def handle(self):
        server_logger.info(f"Connected with: {self.client_address}")

        while True:
            msg = self.recv_str()
            if not msg:
                server_logger.info(f"Connection closed with: {self.client_address}")
                break

            msg = json.loads(msg)

            if msg['type'] == 'SERVER_INFO':
                self.send_server_info()

            elif msg['type'] == 'CONNECT_VIDEO':
                self.establish_video(msg['to'])

    def establish_video(self, client_port):
        monitor = get_monitors()[0]
        client_ip = list(self.client_address)[0]
        command_str = \
            f"ffmpeg -loglevel quiet -video_size {monitor.width}x{monitor.height} -framerate 25 -f x11grab -i :0.0 -vf \
            scale=1366:768 -vcodec libx264 -pix_fmt yuv420p -tune zerolatency -preset ultrafast \
            -f mpegts udp://{client_ip}:{client_port}"
        video_streamer = subprocess.Popen(command_str.split())
        server_logger.info(f"UDP Video stream started: {self.client_address} : sending video stream to client port({client_port})")
        while True:
            self.send_str('ok')
            response = self.recv_str()
            if not response or response != 'play':
                video_streamer.kill()
                server_logger.info(f"UDP Video stream stopped: {self.client_address}")
                break

            sleep(1)

    def send_server_info(self):
        monitor = get_monitors()[0]

        server_info = {
            'resolution': {'height': monitor.height, 'width': monitor.width}
        }
        self.send_str(json.dumps(server_info))

    def recv_data(self):
        data = self.request.recv(8192)
        if not data:
            return None

        return data

    def recv_str(self):
        data = self.recv_data()
        if not data:
            return None

        return data.decode()

    def send_str(self, text, logger=None):
        self.request.send(text.encode())
        if logger: logger.info(f'Message sent to:{self.client_address} Message: {text}')


class Server:
    def __init__(self, port):
        server_logger.info('listening to connections...')
        TCPServer.allow_reuse_address = True
        self.serve = TCPServer(('', port), ServerRequestHandler)

    def run(self):
        self.serve.serve_forever()