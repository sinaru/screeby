from threading import Thread
from screeby.network import tcp_sock
import json
from time import sleep
from collections import deque
from screeby.mouse_sinals import *


class RemoteMouse(Thread):
    def __init__(self, address, logger=None):
        super().__init__()
        self.address = address
        self.logger = logger
        self.event_data = deque()
        self.position = None
        self.user_stop_signal = False

    def run(self):
        with tcp_sock(self.address, no_delay=True) as s:
            js = json.dumps({'type': 'CONNECT_MOUSE'})
            s.send(js.encode())
            data = s.recv(16)
            if not data:
                return

            message = data.decode()
            if message != 'ok':
                return

            while not self.should_stop():
                self.send_mouse_data(s)

    def set_position(self, event):
        self.event_data.append(event)

    def set_click_data(self, event):
        self.event_data.append(event)

    def send_mouse_data(self, socket):
        msg = self.click_data_bytes()
        if msg is None:
            return

        if msg is not None: self.send_data(msg, socket)

    def click_data_bytes(self):
        if len(self.event_data) == 0:
            return None

        data = MOUSE_CLICK

        event = self.event_data.popleft()

        if hasattr(event, 'name'):
            if event.name == 'left':
                data += MOUSE_LEFT
            else:
                data += MOUSE_RIGHT

            if event.press:
                data += MOUSE_CLICK
            else:
                data += MOUSE_RELEASE

            return data + b'\x00\x00'
        else:
            return MOUSE_POSITION + \
                   (event.x).to_bytes(2, byteorder='big') + \
                   (event.y).to_bytes(2,byteorder='big')

    def pop_position(self):
        position = self.position
        if position is None:
            return None

        self.position = None

        return position

    def send_data(self, data, socket):
        socket.send(data)
        if self.logger: self.logger.info(f"mouse data sent - {data}")

    def stop(self):
        self.user_stop_signal = True

    def should_stop(self):
        return self.user_stop_signal
