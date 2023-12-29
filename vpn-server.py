import json
import os

from protocols.udpprotocol import UDPProtocol
from core import User, VPNData


class VPNServer:
    def __init__(self, protocol: UDPProtocol):
        self.users = []
        self.protocol = protocol

    def start(self):
        print('Starting VPN server...')

        for data in self.protocol.start():
            try:
                vpn_data = VPNData.to_instance(json.loads(data))
                self.__request(vpn_data)
            except Exception as e:
                print(f"Error: {e}")
                continue

    def stop(self):
        self.protocol.stop()
        print('VPN server stopped')

    def create_user(self, id: int, username: str, password: str, vlan_id: int):
        if any(user.id == id for user in self.users):
            print('User already registered')
            return

        self.users.append(User(id, username, password, vlan_id))
        print(f"User {username} created with VLAN {vlan_id}")

    def remove_user(self, id):
        if not any(user.id == id for user in self.users):
            print(f"The user with id {id} not exists")
            return

        self.users = list(filter(lambda x: x.id == id, self.users))

    def __request(self, vpn_data: VPNData):
        user = next(
            filter(lambda x: x.username == vpn_data.username and x.password == vpn_data.password, self.users), None
        )

        if user is None:
            print('User not found or password incorrect')
            return

        self.protocol.send(vpn_data.data, vpn_data.dip, vpn_data.dport)

    def __read_users(self) -> list[User]:
        data_path: str = 'data/users.json'
        if not os.path.exists(data_path):
            return []

        try:
            with open(data_path, 'r') as file:
                return list(
                    map(
                        lambda x: User.to_instance(x),
                        json.loads(file.read())
                    )
                )

        except Exception as e:
            print(f"Error: Corrupt Data: {e}")
            return []

    def __write_users(self):
        data_path: str = 'data/users.json'

        with open(data_path, 'w') as file:
            json.dump(self.users, file, default=lambda x: x.__dict__)
