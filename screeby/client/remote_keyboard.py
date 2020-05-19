from threading import Thread
from pynput import keyboard
from screeby.network import make_tcp_sock
import json
from time import sleep


class RemoteKeyboard(Thread):
    def __init__(self, address, logger=None):
        Thread.__init__(self)
        self.user_signal_stop = False
        self.address = address
        self.logger = logger
        self.sock = make_tcp_sock(self.address)

    def run(self):
        js = json.dumps({'type': 'CONNECT_KEYBOARD'})
        self.sock.send(js.encode())
        data = self.sock.recv(16)
        if not data:
            return
        message = data.decode()
        if message == 'ok':
            if self.logger: self.logger.info('keyboard connection established')
        else:
            if self.logger: self.logger.info('keyboard connection failed')

        break_listen = False

        listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)

        listener.start()

        while not self.user_signal_stop:
            sleep(0.005)

        listener.stop()

        if self.logger: self.logger.info('Closing keyboard connection')

    def on_press(self, key):
        self.send_key(key, 'press')

    def on_release(self, key):
        self.send_key(key, 'release')

    def send_key(self, key, event_name):
        if hasattr(key, 'char'):
            key_char = key.char
        else:
            key_char = key.name
        message = f"{event_name}|{key_char}"
        if self.logger: self.logger.info("SEND KEY: ", message)
        self.sock.send(str.encode(message))
        data = self.sock.recv(10)

    def stop(self):
        self.user_signal_stop = True
