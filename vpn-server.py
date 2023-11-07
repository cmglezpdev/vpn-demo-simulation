from tcpprotocol import TCPProtocol
from udpprotocol import UDPProtocol

class VPNServer:
    def __init__(self):
        self.users = {} # Diccionario para almacenar los usuarios y sus VLANs
        self.vlan_restrictions = {} # Diccionario para restricciones de VLAN
        self.user_restrictions = {} # Diccionario para restricciones de usuario

    def start(self, protocol_type):
        if protocol_type == 'use_tcp':
            self.protocol = TCPProtocol('localhost', 12345)
        elif protocol_type == 'use_upd':
            self.protocol = UDPProtocol('localhost', 12345)
        else:
            print('Protocol is not supported.')
            return
        print(f"VPN server started using {protocol_type}") 

        while True:
            command = input('Enter command: ').split()
            if command[0] == 'create_user':
                name, password, vlan_id = command[1], command[2], command[3]
                self.create_user(name, password, vlan_id)
            elif command[0] == 'resctrict_vlan':
                vlan_id, ip_network = command[1], command[2]
                self.restrict_vlan(vlan_id, ip_network)
            elif command[0] == 'restrict_user':
                user_id, ip_network = command[1], command[2]
                self.restrict_user(user_id, ip_network)
            elif command[0] == 'stop':
                self.stop()
                break
            else:
                print('Invalid command')      


    def create_user(self, name, password, vlan_id):
        self.users[name] = (password, vlan_id)
        print(f"User {name} created with VLAN {vlan_id}")

    def restrict_vlan(self, vlan_id, ip_network):
        self.vlan_restrictions[vlan_id].add(ip_network)
        print(f"VLAN ${vlan_id} was restricted by IP ${ip_network}")

    def restrict_user(self, user_id, ip_network):
        self.user_restrictions[user_id].add(ip_network)
        print(f"User ${user_id} was restricted by IP ${ip_network}")
        
    def stop(self):
        self.protocol.stop()


# server = VPNServer()
# server.start(protocol_type='use_tcp')