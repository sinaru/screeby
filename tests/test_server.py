from unittest.mock import *
import unittest
from screeby.server.server import Server
from screeby.server.server import ServerRequestHandler


class ServerTestCase(unittest.TestCase):
    @patch('screeby.server.server.ThreadingTCPServer')
    def setUp(self, tcp_server_mock) -> None:
        self.server = Server(5555)
        self.tcp_server_klass = tcp_server_mock
        self.tcp_server = tcp_server_mock.return_value

    def test__init__method(self):
        self.tcp_server_klass.assert_called_once_with(('', 5555), ServerRequestHandler)

    def test_run_method(self):
        self.server.run()
        self.server.serve.serve_forever.assert_called_once()

    def test_stopping_server(self):
        self.server.stop()
        self.tcp_server.shutdown.assert_called_once()
