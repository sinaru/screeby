from pynput.mouse import Button, Controller as MouseController
from time import sleep
from screeby.mouse_sinals import *

class MouseReceiver:
    def __init__(self, request, logger = None):
        self.request = request
        self.logger = logger
        self.delay = 1/120
        self.mouse = MouseController()

    def run(self):
        while True:
            data = self.request.recv(5*5)
            if not data:
                break

            for d in self.chunks(data, 5):
                key, *event_data = d

                if key == MOUSE_POSITION:
                    x = int.from_bytes(event_data[:2], byteorder='big')
                    y = int.from_bytes(event_data[2:4], byteorder='big')
                    self.mouse.position = (x, y)
                if key == MOUSE_CLICK:
                    pressed = True if event_data[1] == MOUSE_CLICK else False
                    if event_data[0] == MOUSE_LEFT:
                        name = 'left'
                    else:
                        name = 'right'
                    if pressed:
                        self.mouse.press(Button[name])
                    else:
                        self.mouse.release(Button[name])

                if self.logger: self.logger.info(f"mouse {data}")
            sleep(self.delay)

    def chunks(self, lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]
