import sqlite3
from core import constants
from enum import Enum
from core.users import UsersDbOperations
from core import VPNData
from abc import ABC, abstractmethod


class RestrictionType(Enum):
    USER = 'USER'
    VLAN = 'VLAN'


class Restriction(ABC):
    def __init__(self, block_ip: str, block_port: int, type: RestrictionType):
        self.ip = block_ip
        self.port = block_port
        self.type = type

    @abstractmethod
    def check_pass(self, request: VPNData):
        raise Exception('Method not implement')

    @abstractmethod
    def to_string(self):
        raise Exception('Method not implement')


class VLANRestriction(Restriction):
    def __init__(self, vlan_id: int, block_ip: str, block_port: int):
        super().__init__(block_ip, block_port, RestrictionType.VLAN)
        self.vlan_id = vlan_id

        self.db_users = UsersDbOperations()

    def check_pass(self, request: VPNData):
        user = self.db_users.get_user(request.username)
        if user is None:
            return False

        is_blocked = user.vlan_id == self.vlan_id and self.ip == request.dip and self.port == request.dport
        return not is_blocked

    def to_string(self):
        return f"VLAN: {self.vlan_id}, IP: {self.ip}, Port: {self.port}"


class UserRestriction(Restriction):
    def __init__(self, username: str, block_ip: str, block_port: int):
        super().__init__(block_ip, block_port, RestrictionType.USER)
        self.username = username

        self.db_users = UsersDbOperations()

    def check_pass(self, request: VPNData):
        user = self.db_users.get_user(request.username)
        if user is None:
            return False

        is_blocked = user.username == self.username and self.ip == request.dip and self.port == request.dport
        return not is_blocked

    def to_string(self):
        return f"USER: {self.username}, IP: {self.ip}, Port: {self.port}"


class RestrictionsDbOperations(ABC):
    """
    This class contains all the database operations related to restrictions.
    """

    def __init__(self):
        self.db_connection = sqlite3.connect(constants.DATABASE_PATH)
        self.db_cursor = self.db_connection.cursor()
        self.restriction_type = RestrictionType

    def restrict_vlan(self, vlan: int, blocked_ip: str, blocked_port: int) -> bool:
        self.db_cursor.execute(
            """
            insert into restrictions(type, blocked_ip, blocked_port, blocked_vlan_id)
            values
            (?, ?, ?, ?)
            """,
            (self.restriction_type.VLAN.value, blocked_ip, blocked_port, vlan)
        )

        self.db_connection.commit()
        return True

    def restrict_user(self, user_id: int, blocked_ip: str, blocked_port: int) -> bool:
        self.db_cursor.execute(
            """
            insert into restrictions(type, blocked_ip, blocked_port, blocked_user_id)
            values
            (?, ?, ?, ?)
            """,
            (self.restriction_type.USER.value, blocked_ip, blocked_port, user_id)
        )

        self.db_connection.commit()
        return True

    def list_restrictions(self, type: RestrictionType = None) -> list[Restriction]:
        if type is not None:
            self.db_cursor.execute("select * from restrictions where type = ?", (type.value,))
        else:
            self.db_cursor.execute("select * from restrictions")

        mapped = list(map(
            lambda row: self.__row_to_dict(row),
            self.db_cursor.fetchall()
        ))

        restrictions: list[Restriction] = []
        for rule in mapped:
            if rule['type'] == RestrictionType.USER.value:
                restrictions.append(UserRestriction(rule['user_id'], rule['blocked_ip'], rule['blocked_port']))
            else:
                restrictions.append(VLANRestriction(rule['vlan_id'], rule['blocked_ip'], rule['blocked_port']))

        return restrictions

    def close(self):
        self.db_connection.close()

    @staticmethod
    def __row_to_dict(row: tuple) -> dict:
        data = {
            'id': row[0],
            'type': row[1],
            'blocked_ip': row[2],
            'blocked_port': row[3],
        }

        if row[1] == RestrictionType.USER.value:
            data['user_id'] = row[4]
        else:
            data['vlan_id'] = row[5]

        return data
