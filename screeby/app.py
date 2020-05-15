import sys
import pathlib
pa = str(pathlib.Path(__file__).parent.parent.absolute())
sys.path.append(pa)

import argparse
import logging
from ipaddress import IPv4Address
from screeby.server.server import Server
from screeby.client import Client

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def main():
    description = '''
        A simple screen sharing and control tool for your local network. By default, Screeby will listen to incoming \
        connections. Otherwise, you can use --connect argument to connect to a host machine that is running Screeby.
    '''
    parser = argparse.ArgumentParser(description)
    parser.add_argument('--connect', help='ip address to connect to (e.g. 127.0.0.1)', type=IPv4Address)
    parser.add_argument('--port', help='port address to host or connect to. By default it is 5005.', default=5005,
                        type=int)
    args = parser.parse_args()

    connect_ip, port = args.connect, args.port

    if connect_ip:
        start_client(str(connect_ip), port)
    else:
        start_server(port)


def start_server(port):
    server = Server(port)
    server.run()

def start_client(ip, port):
    client = Client(ip, port)
    client.run()


if __name__ == "__main__":
    main()
