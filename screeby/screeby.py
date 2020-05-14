import argparse
from ipaddress import IPv4Address


def main():
    description = '''
        A simple screen sharing and control tool for your local network. By default, Screeby will listen to 
        incoming connections. Otherwise, you can use --connect argument to connect to a host machine that is running 
        Screeby.
    '''
    parser = argparse.ArgumentParser(description)
    parser.add_argument('--connect', help='ip address to connect to (e.g. 127.0.0.1)', type=IPv4Address)
    parser.add_argument('--port', help='port address to host or connect to. By default it is 5005.', default=5005,
                        type=int)
    args = parser.parse_args()

    connect_ip, port_number = args.connect, args.port


if __name__ == "__main__":
    main()
