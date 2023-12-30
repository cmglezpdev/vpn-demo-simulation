from protocols import UDPProtocol
import sys

protocol = UDPProtocol('127.0.0.1', 3002)

args = sys.argv[1:]

if len(args) == 0:
    print("Invalid protocols")
    exit(1)

if args[0] == 'udp':
    print('Server UDP started')
    for data in protocol.start():
        print(f"Data received: {data}")
else:
    print("Invalid protocol")
    exit(1)
