import json
from protocols.udpprotocol import UDPProtocol
from core.users import UsersDbOperations
from rules.rules import RestrictionsDbOperations, RestrictionType
from core.vpndata import VPNData


class VPNServer:
    def __init__(self, protocol: UDPProtocol):
        self.protocol = protocol
        self.db_users = UsersDbOperations()
        self.db_rules = RestrictionsDbOperations()

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

    def restrict_user(self, username: str, blocked_ip: str, blocked_port: int):
        user = self.db_users.get_user(username)
        if not user:
            print(f'The user {username} not exists')
            return

        self.db_rules.restrict_user(user.id, blocked_ip, blocked_port)
        print(f"User {username} restricted for the address {blocked_ip}:{blocked_port}")

    def restrict_vlan(self, vlan: int, blocked_ip: str, blocked_port: int):
        self.db_rules.restrict_vlan(vlan, blocked_ip, blocked_port)
        print(f"VLAN {vlan}'s users are restricted for the address {blocked_ip}:{blocked_port}")

    def list_restrictions(self, type: str = None):
        restrictions = self.db_rules.list_restrictions(RestrictionType(type) if type else None)
        user_restrictions = list(filter(lambda x: x.type == RestrictionType.USER, restrictions))
        vlan_restrictions = list(filter(lambda x: x.type == RestrictionType.VLAN, restrictions))

        print("Restrictions: ")
        if not type or type == RestrictionType.USER.value:
            print("Users: ")
            for restriction in user_restrictions:
                print(restriction.to_string())

        if not type or type == RestrictionType.VLAN.value:
            print("VLANs: ")
            for restriction in vlan_restrictions:
                print(restriction.to_string())

    def __redirect(self, vpn_data: VPNData):
        logged = self.db_users.login(vpn_data.username, vpn_data.password)

        if logged:
            print('User not found or password incorrect')
            return

        pass_restrictions = any(map(
            lambda x: x.check_pass(vpn_data),
            self.db_rules.list_restrictions()
        ))

        if pass_restrictions:
            self.protocol.send(vpn_data.data, vpn_data.dip, vpn_data.dport)
        else:
            print(f"User {vpn_data.username} restricted for the address {vpn_data.dip}:{vpn_data.dport}")
