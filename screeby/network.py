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
