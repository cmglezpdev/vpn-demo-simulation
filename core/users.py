

class User:
    """
    This class represents a User object.

    Attributes:
        username (str): The username of the user.
        password (str): The password of the user.
        vlan_id (int): The VLAN ID associated with the user.
    """
    def __init__(self, username: str, password: str, vlan_id: int):
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
            user_data_dict['username'],
            user_data_dict['password'],
            user_data_dict['vlan_id']
        )
