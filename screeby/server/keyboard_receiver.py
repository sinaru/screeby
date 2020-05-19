from pynput.keyboard import Key, Controller as KeyboardController
from threading import Thread

class KeyboardReceiver(Thread):
    def __init__(self, request, logger = None):
        Thread.__init__(self)
        self.request = request
        self.logger = logger
        # self.ip = ip
        # self.port = port
        if self.logger : self.logger.info(f"[+] Keyboard listening started")

    def run(self):
        keyboard = KeyboardController()
        while True:
            data = self.request.recv(128)
            if not data:
                if self.logger: self.logger.info(f"Keyboard listening lost")
                break
            message = data.decode()
            type, code = message.split('|')

            code = self.code_to_key(code)
            if code is not None:
                if type == 'press':
                    keyboard.press(code)
                elif type == 'release':
                    keyboard.release(code)
            self.request.send(b"ok")

    def code_to_key(self, key_code):
        if len(key_code) > 1:
            item = getattr(Key, key_code, None)
            if item is None:
                if self.logger: self.logger.error(f"Unknown key {key_code}")
                return None
            return item
        else:
            return key_code
