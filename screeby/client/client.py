import json
import logging
from screeby.client.remote_video import RemoteVideo
from screeby.client.remote_mouse import RemoteMouse
from screeby.client.remote_keyboard import RemoteKeyboard
from screeby.network import response
from screeby.client.ui import RemoteScreen


class Client:
    def __init__(self, ip, port, in_port=8080):
        self.client_logger = logging.getLogger('screeby.Client')
        self.ip = ip
        self.port = port
        self.video_in_port = in_port

    def server_addr(self):
        return (self.ip, self.port)

    def run(self):
        self.s_info = self.server_info()

        threads = []
        self.remote_video = self.connect_video()
        threads.append(self.remote_video)

        self.remote_keyboard = self.connect_keyboard()
        threads.append(self.remote_keyboard)

        self.remote_mouse = self.connect_mouse()
        threads.append(self.remote_mouse)

        screen = self.render_remote_screen()
        screen.on_mouse_move(self.remote_mouse.set_position)
        screen.on_mouse_click(self.remote_mouse.set_click_data)
        screen.on_mouse_release(self.remote_mouse.set_click_data)
        screen.wait_until_closed()

        for t in threads:
            t.stop()

        for t in threads:
            t.join()

    def stop(self):
        pass

    def render_remote_screen(self):
        s_width = self.s_info['resolution']['width']
        s_height = self.s_info['resolution']['height']
        return RemoteScreen(f"Remote Screen: {self.ip}", f"udp://127.0.0.1:{self.video_in_port}",
                            s_width, s_height,
                            play=True)

    def connect_video(self):
        thread = RemoteVideo(self.server_addr(), logger=self.client_logger, client_port=self.video_in_port)
        thread.start()
        return thread

    def connect_mouse(self):
        thread = RemoteMouse(self.server_addr())
        thread.start()
        return thread

    def connect_keyboard(self):
        thread = RemoteKeyboard(self.server_addr())
        thread.start()
        return thread

    def server_info(self):
        js = json.dumps({'type': 'SERVER_INFO'})
        message = response(self.server_addr(), js)
        if not message:
            return None

        self.client_logger.info(f"{self.server_addr()} : Got server info: {message}")
        return json.loads(message)
