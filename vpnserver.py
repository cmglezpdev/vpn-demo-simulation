import json
from protocols.udpprotocol import UDPProtocol
from core.users import UsersDbOperations
from core.vpndata import VPNData


class VPNServer:
    def __init__(self, protocol: UDPProtocol):
        self.protocol = protocol
        self.db_users = UsersDbOperations()

    def start(self):
        print('VPN server started...')

        for data in self.protocol.start():
            try:
                vpn_data = VPNData.to_instance(json.loads(data))
                self.__redirect(vpn_data)
            except Exception as e:
                print(f"Error: {e}")
                continue

    def stop(self):
        self.protocol.close()
        self.db_users.close()
        print('VPN server stopped')

    def create_user(self, username: str, password: str, vlan_id: int):
        user_exists = self.db_users.get_user(username)

        if user_exists:
            print('User already registered.')
            return

        self.db_users.create_user(username, password, vlan_id)
        print(f"User {username} created with VLAN {vlan_id}")

    def remove_user(self, username: str):
        user_exists = self.db_users.get_user(username)

        if not user_exists:
            print(f"The user with username {username} not exists")
            return

        self.db_users.remove_user(username)
        print(f"User {username} removed")

    def list_users(self, vlan_id: int = None):
        users = self.db_users.list_users(vlan_id)

        print("Users: ")
        for user in users:
            print(f"Username: {user.username}, VLAN: {user.vlan_id}")

    def __redirect(self, vpn_data: VPNData):
        logged = self.db_users.login(vpn_data.username, vpn_data.password)

        if logged:
            print('User not found or password incorrect')
            return

        self.protocol.send(vpn_data.data, vpn_data.dip, vpn_data.dport)
