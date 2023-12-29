

class User:
    def __init__(self, id: int, username: str, password: str, vlan_id: int):
        self.username = username
        self.password = password
        self.vlan_id = vlan_id
        self.id = id

    @staticmethod
    def to_instance(user_data_dict: dict) -> 'User':
        return User(
            user_data_dict['id'],
            user_data_dict['username'],
            user_data_dict['password'],
            user_data_dict['vlan_id']
        )
