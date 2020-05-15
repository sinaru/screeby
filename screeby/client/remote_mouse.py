from threading import Thread
from screeby.network import sock
import json
from time import sleep
from collections import deque


class RemoteMouse(Thread):
    def __init__(self, address, logger=None):
        super().__init__()
        self.address = address
        self.logger = logger
        self.click_data = deque()
        self.position = None
        self.user_stop_signal = False

    def run(self):
        with sock(self.address) as s:
            js = json.dumps({'type': 'CONNECT_MOUSE'})
            s.send(js.encode())
            data = s.recv(1024)
            if not data:
                return

            message = data.decode()
            if message != 'ok':
                return

            while not self.should_stop():
                self.send_from_mouse_position(s)
                self.delay = 0.001
                sleep(self.delay)

    def set_position(self, event):
        self.position = event

    def set_click_data(self, event):
        self.click_data.append(event)

    def send_from_mouse_position(self, socket):

        click_msg = self.click_message()
        pos_msg = self.position_message()
        if pos_msg is None and click_msg is None:
            return

        if pos_msg is not None: self.send_mouse_message(pos_msg, socket)
        if click_msg is not None: self.send_mouse_message(click_msg, socket)

    def click_message(self):
        if len(self.click_data) == 0:
            return None

        click = self.click_data.popleft()

        return f"click|{click.name}|{click.press}"

    def position_message(self):
        position = self.position
        if position is None:
            return None

        self.position = None
        return f"move|{position.x}|{position.y}"

    def send_mouse_message(self, message, socket):
        socket.send(str.encode(message))
        if self.logger: self.logger.info("mouse data sent - ", message)
        data = socket.recv(10)

    def stop(self):
        self.user_stop_signal = True

    def should_stop(self):
        return self.user_stop_signal
