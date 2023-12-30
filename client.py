from protocols import UDPProtocol
from core import VPNData
import json
import sys

username = input('Username: ')
password = input('Password: ')

destination_ip = input('Destination IP: ')
destination_port = int(input('Destination Port: '))
data = input('Data: ')

protocol = UDPProtocol('127.0.0.1', 3000)

vpn_data = json.dumps(
    VPNData(username, password, destination_ip, destination_port, data),
    default=lambda x: x.__dict__
)

args = sys.argv[1:]
if len(args) == 0:
    print("Invalid protocols")
    exit(1)

if args[0] == 'udp':
    protocol.send(vpn_data, '127.0.0.1', 3001)
else:
    print("Invalid protocol")
    exit(1)
