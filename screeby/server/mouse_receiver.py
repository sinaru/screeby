from pynput.mouse import Button, Controller as MouseController
from time import sleep

class MouseReceiver:
    def __init__(self, request, logger = None):
        self.request = request
        self.logger = logger
        self.delay = 0.0166
        self.mouse = MouseController()

    def run(self):
        while True:
            data = self.request.recv(8192)
            if not data:
                break

            message = data.decode()
            key, *event_data = message.split('|')

            if key == 'move':
                x, y = event_data
                self.mouse.position = (int(x), int(y))

            if key == 'click':
                pressed = True if event_data[1] == 'true' else False
                name = event_data[0]
                if pressed:
                    self.mouse.press(Button[name])
                else:
                    self.mouse.release(Button[name])

            if self.logger: self.logger.info(f"MOUSE SIG: {message}")
            self.request.send('ok'.encode())
            sleep(self.delay)
