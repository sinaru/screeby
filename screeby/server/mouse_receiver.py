from pynput.mouse import Button, Controller as MouseController
from time import sleep

class MouseReceiver:
    def __init__(self, request, logger = None):
        self.request = request
        self.logger = logger
        self.delay = 1/120
        self.mouse = MouseController()

    def run(self):
        while True:
            data = self.request.recv(1024)
            if not data:
                break

            for d in self.chunks(data, 32):
                message = d.decode()
                key, *event_data = message.split('|')

                if key == 'move':
                    x, y = event_data[0], event_data[1]
                    self.mouse.position = (int(x), int(y))

                if key == 'click':
                    pressed = True if event_data[1] == 'true' else False
                    name = event_data[0]
                    if pressed:
                        self.mouse.press(Button[name])
                    else:
                        self.mouse.release(Button[name])

                if self.logger: self.logger.info(f"mouse {message}")
            sleep(self.delay)

    def chunks(self, lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]
