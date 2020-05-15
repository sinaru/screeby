import json
import logging
from screeby.remote_video import RemoteVideo
from screeby.network import response
from screeby.ui.remote_screen import RemoteScreen
client_logger = logging.getLogger('screeby.Client')


class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.video_in_port = '5007'

    def server_addr(self):
        return (self.ip, self.port)

    def run(self):
        self.s_info = self.server_info()

        threads = []
        self.remote_video = self.connect_video()
        threads.append(self.remote_video)

        screen = self.render_remote_screen()
        screen.wait_until_closed()

        for t in threads:
            t.kill()

        for t in threads:
            t.join()

    def render_remote_screen(self):
        return RemoteScreen(f"Remote Screen: {self.ip}", f"udp://127.0.0.1:{self.video_in_port}")

    def connect_video(self):
        thread = RemoteVideo(self.server_addr(), logger=client_logger, client_port=self.video_in_port)
        thread.start()
        return thread

    def server_info(self):
        js = json.dumps({'type': 'SERVER_INFO'})
        message = response(self.server_addr(), js)
        if not message:
            return None

        client_logger.info(f"{self.server_addr()} : Got server info: {message}")
        return json.loads(message)
