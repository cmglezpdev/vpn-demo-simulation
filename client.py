from protocols import UDPProtocol
from core import VPNData
import json

# username = input('Username: ')
# password = input('Password: ')
#
# destination_ip = input('Destination IP: ')
# destination_port = int(input('Destination Port: '))
# data = input('Data: ')

username = 'unlock_user'
password = '123'
destination_ip = '127.0.0.1'
destination_port = 3002
data = 'Esta es la data'

protocol = UDPProtocol('127.0.0.1', 3000)

vpn_data = json.dumps(
    VPNData(username, password, destination_ip, destination_port, data),
    default=lambda x: x.__dict__
)

protocol.send(vpn_data, '127.0.0.1', 3002)
