import sqlite3
from abc import ABC
from typing import Union
from core import constants


class User:
    """
    This class represents a User object.

    Attributes:
        username (str): The username of the user.
        password (str): The password of the user.
        vlan_id (int): The VLAN ID associated with the user.
    """

    def __init__(self, id: int, username: str, password: str, vlan_id: int):
        super().__init__()
        self.id = id
        self.username = username
        self.password = password
        self.vlan_id = vlan_id

    @staticmethod
    def to_instance(user_data_dict: dict) -> 'User':
        """
        Creates a new User instance from a dictionary.

        Parameters:
            user_data_dict (dict): A dictionary containing the user data.

        Returns:
            User: A new User instance.
        """
        return User(
            user_data_dict['id'],
            user_data_dict['username'],
            user_data_dict['password'],
            user_data_dict['vlan_id']
        )


class UsersDbOperations(ABC):
    """
    This class contains all the database operations related to users.
    """

    def __init__(self):
        self.db_connection = sqlite3.connect(constants.DATABASE_PATH)
        self.db_cursor = self.db_connection.cursor()

    def get_user(self, username: str) -> Union[User, None]:
        self.db_cursor.execute(
            """
            select * from users
            where username = ?
            """,
            (username,)
        )

        user_data = self.db_cursor.fetchone()
        if user_data is None:
            return None

        return User.to_instance(self.__row_to_dict(user_data))

    def create_user(self, username: str, password: str, vlan_id: int) -> bool:
        exists = self.get_user(username)
        if exists is not None:
            return False

        self.db_cursor.execute(
            """
            insert into users(username, password, vlan_id)
            values 
            (?, ?, ?)
            """,
            (username, password, vlan_id)
        )

        self.db_connection.commit()
        return True

    def remove_user(self, username: str) -> bool:
        exists = self.get_user(username)
        if exists is None:
            return False

        self.db_cursor.execute("delete from users where username = ?", (username,))
        self.db_connection.commit()
        return True

    def list_users(self, vlan_id: int = None) -> list[User]:
        if vlan_id is not None:
            self.db_cursor.execute("select * from users where vlan_id = ?",(vlan_id,))
        else:
            self.db_cursor.execute("select * from users")

        return list(map(
            lambda x: User.to_instance(self.__row_to_dict(x)),
            self.db_cursor.fetchall()
        ))

    def login(self, username: str, password: str) -> bool:
        user = self.get_user(username)
        if user is None:
            return False

        return user['password'] == password

    def restrict_user(self, username: str, blocked_ip: str, blocked_port: int) -> bool:
        exists = self.get_user(username)
        if exists is None:
            return False

        self.db_cursor.execute(
            """
            insert into restrictions(type, blocked_ip, blocked_port, blocked_user_id)
            values
            (?, ?, ?, ?)
            """,
            (self.restriction_type.USER, blocked_ip, blocked_port, exists['id'])
        )

        self.db_connection.commit()
        return True

    def close(self):
        self.db_connection.close()

    @staticmethod
    def __row_to_dict(row: tuple) -> dict:
        return {
            'id': row[0],
            'username': row[1],
            'password': row[2],
            'vlan_id': row[3]
        }
