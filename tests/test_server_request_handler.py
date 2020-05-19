from unittest.mock import *
import unittest
from types import SimpleNamespace
from screeby.server.server import ServerRequestHandler


class ServerRequestHandlerTest(unittest.TestCase):
    def get_handler(self):
        return ServerRequestHandler(request=self.request_mock,
                                    client_address=self.address_mock,
                                    server=self.server_mock)

    def setUp(self) -> None:
        self.request_mock = MagicMock()
        self.server_mock = MagicMock()
        self.address_mock = MagicMock()

    @patch('screeby.server.server.get_monitors')
    def test_server_info_request(self, monitor):
        screen = SimpleNamespace(height=1000, width=1000)
        monitor.return_value = [screen]
        self.request_mock.recv.return_value = '{"type": "SERVER_INFO"}'.encode()
        self.get_handler()
        self.request_mock.send.assert_called_once_with(
            b'{"resolution": {"height": 1000, "width": 1000}}'
        )
