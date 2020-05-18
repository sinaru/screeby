from unittest.mock import *
import unittest

class ServerTestCase(unittest.TestCase):
    def test__init__method(self):
        with patch('socketserver.ThreadingTCPServer') as mock:
            from screeby.server.server import Server, ServerRequestHandler
            Server(5555)
            mock.assert_called_once_with(('', 5555), ServerRequestHandler)

    @patch('socketserver.ThreadingTCPServer')
    def test_run_method(self, _mock):
        from screeby.server.server import Server
        server = Server(5555)
        server.run()
        server.serve.serve_forever.assert_called_once()
