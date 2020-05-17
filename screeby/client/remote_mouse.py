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
        self.click_data = deque()
        self.position = None
        self.user_stop_signal = False
        self.delay = 1 / 120

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
                sleep(self.delay)

    def set_position(self, event):
        self.position = event

    def set_click_data(self, event):
        self.click_data.append(event)

    def send_mouse_data(self, socket):
        click_msg = self.click_data_bytes()
        pos_msg = self.position_data_bytes()
        if pos_msg is None and click_msg is None:
            return

        if pos_msg is not None: self.send_mouse_message(pos_msg, socket)
        if click_msg is not None: self.send_mouse_message(click_msg, socket)

    def click_data_bytes(self):
        if len(self.click_data) == 0:
            return None

        data = MOUSE_CLICK

        click = self.click_data.popleft()

        if click.name == 'left':
            data += MOUSE_LEFT
        else:
            data += MOUSE_RIGHT

        if click.press:
            data += MOUSE_CLICK
        else:
            data += MOUSE_RELEASE

        return data + b'\x00\x00'

    def position_data_bytes(self):
        position = self.pop_position()
        if position is None: return None

        return MOUSE_POSITION + (position.x).to_bytes(2, byteorder='big') + (position.y).to_bytes(2, byteorder='big')

    def pop_position(self):
        position = self.position
        if position is None:
            return None

        self.position = None

        return position

    def send_mouse_message(self, data, socket):
        socket.send(data)
        if self.logger: self.logger.info(f"mouse data sent - {data}")
        # data = socket.recv(1)
        sleep(self.delay)

    def stop(self):
        self.user_stop_signal = True

    def should_stop(self):
        return self.user_stop_signal
