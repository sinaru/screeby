import socket
from contextlib import contextmanager


@contextmanager
def tcp_sock(address, logger=None, no_delay=False):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if no_delay:
        s.setsockopt(socket.SOL_TCP, socket.TCP_QUICKACK, 1)
        s.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
    try:
        s.connect(address)
        if logger: logger.info(f"{address} : Connected")
        yield s
    finally:
        s.close()


def response(address: tuple, message: str, decode: bool = True, logger=None):
    with tcp_sock(address) as s:
        s.send(message.encode())
        message = s.recv(8192)

    if not message:
        return None

    if decode:
        message = message.decode()
        if logger: logger.info(f"{address} : Got response : {message}")

    return message
