import json
from threading import Thread
from screeby.network import sock


class RemoteVideo(Thread):
    def __init__(self, address, logger=None, client_port = '5007'):
        super().__init__()
        self.__kill = False
        self.client_port = client_port
        self.logger = logger
        self.address = address

    def kill(self):
        self.__kill = True

    def should_die(self):
        return self.__kill

    def run(self):
        with sock(self.address) as s:
            js = json.dumps({'type': 'CONNECT_VIDEO', 'to': self.client_port})
            s.send(js.encode())
            data = s.recv(1024)
            if not data:
                return

            message = data.decode()
            if message != 'ok':
                return

            while not self.should_die():
                s.send('play'.encode())
                data = s.recv(1024)
                if not data:
                    break
