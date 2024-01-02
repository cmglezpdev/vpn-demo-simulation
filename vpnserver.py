import json
import os
from pathlib import Path
from protocols.udpprotocol import UDPProtocol
from core.users import User
from core.vpndata import VPNData
import core.constants as constants


class VPNServer:
    def __init__(self, protocol: UDPProtocol):
        self.users = self.__read_users()
        self.protocol = protocol

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
        print('VPN server stopped')

    def create_user(self, username: str, password: str, vlan_id: int):
        if any(user.username == username for user in self.users):
            print('User already registered')
            return

        self.users.append(User(username, password, vlan_id))
        self.__write_users()
        print(f"User {username} created with VLAN {vlan_id}")

    def remove_user(self, username: str):
        if not any(user.username == username for user in self.users):
            print(f"The user with username {username} not exists")
            return

        self.users = list(filter(lambda x: x.username == username, self.users))
        self.__write_users()
        print(f"User {username} removed")

    def list_users(self, vlan_id: int = None):
        filtered_users = list(filter(
            lambda x: vlan_id is None or x.vlan_id == vlan_id,
            self.users
        ))
        print("Users: ")
        for user in filtered_users:
            print(f"Username: {user.username}, VLAN: {user.vlan_id}")

    def __redirect(self, vpn_data: VPNData):
        user = next(
            filter(lambda x: x.username == vpn_data.username and x.password == vpn_data.password, self.users), None
        )

        if user is None:
            print('User not found or password incorrect')
            return

        self.protocol.send(vpn_data.data, vpn_data.dip, vpn_data.dport)

    def __read_users(self) -> list[User]:
        if not os.path.exists(constants.USERS_DATA_PATH):
            return []

        try:
            with open(constants.USERS_DATA_PATH, 'r') as file:
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
        Path(constants.USERS_DATA_PATH).parent.mkdir(parents=True, exist_ok=True)

        with open(constants.USERS_DATA_PATH, 'w+') as file:
            json.dump(self.users, file, default=lambda x: x.__dict__)
