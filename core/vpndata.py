
class VPNData:
    """
    This class represents data of manage for the vpn.

    Attributes:
        username (str): The username's user.
        password (str): The password's user.
        dip (str): The destination IP address for the VPN connection.
        dport (int): The destination port for the VPN connection.
        data (str): Data that the user wants to send.
    """
    def __init__(self, username: str, password: str, dip: str, dport: int, data: str):
        self.username = username
        self.password = password
        self.dip = dip
        self.dport = dport
        self.data = data

    @staticmethod
    def to_instance(vpn_data_dict: dict) -> 'VPNData':
        """
        Creates a new VPNData instance from a dictionary.

        Parameters:
            vpn_data_dict (dict): A dictionary containing the VPN data.

        Returns:
            VPNData: A new VPNData instance.
        """
        return VPNData(
            vpn_data_dict['username'],
            vpn_data_dict['password'],
            vpn_data_dict['dip'],
            vpn_data_dict['dport'],
            vpn_data_dict['data']
        )
