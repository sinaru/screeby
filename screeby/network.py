from socket import socket, AF_INET, SOCK_STREAM
from contextlib import contextmanager


@contextmanager
def sock(address, logger=None):
    s = socket(AF_INET, SOCK_STREAM)
    try:
        s.connect(address)
        if logger: logger.info(f"{address} : Connected")
        yield s
    finally:
        s.close()


def response(address: tuple, message: str, decode: bool = True):
    with sock(address) as s:
        s.send(message.encode())
        message = s.recv(8192)

    if not message:
        return None

    if decode:
        return message.decode()

    return message
