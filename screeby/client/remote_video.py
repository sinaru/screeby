import json
from threading import Thread
from screeby.network import tcp_sock
from time import sleep

class RemoteVideo(Thread):
    def __init__(self, address, logger=None, client_port = '5007'):
        super().__init__()
        self.alive_video_check_delay = 1 # seconds
        self.user_stop_signal = False
        self.client_port = client_port
        self.logger = logger
        self.address = address

    def stop(self):
        self.user_stop_signal = True

    def should_stop(self):
        return self.user_stop_signal

    def run(self):
        with tcp_sock(self.address) as s:
            js = json.dumps({'type': 'CONNECT_VIDEO', 'to': self.client_port})
            s.send(js.encode())
            data = s.recv(1024)
            if not data:
                return

            message = data.decode()
            if message != 'ok':
                return

            while not self.should_stop():
                s.send('play'.encode())
                data = s.recv(1024)
                if not data:
                    break
                sleep(self.alive_video_check_delay)
