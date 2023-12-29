
class VPNData:
    def __init__(self, username: str, password: str, dip: str, dport: int, data: str):
        self.username = username
        self.password = password
        self.dip = dip
        self.dport = dport
        self.data = data

    @staticmethod
    def to_instance(vpn_data_dict: dict) -> 'VPNData':
        return VPNData(
            vpn_data_dict['username'],
            vpn_data_dict['password'],
            vpn_data_dict['dip'],
            vpn_data_dict['dport'],
            vpn_data_dict['data']
        )
