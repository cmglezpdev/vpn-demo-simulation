import uuid
from core import User, IPAddress
#
#
# class VLANRestriction:
#     def __init__(self, vlan_id: int, restricted_ip: IPAddress):
#         self.vlan_id = vlan_id
#         self.restricted_ip = restricted_ip
#
#     def check(self, user: User, ip_dest: IPAddress) -> bool:
#         return user.vlan_id == self.vlan_id and self.restricted_ip.is_in_subnet(ip_dest.ip)
#
#
# class UserRestriction:
#     def __init__(self, user_id: int, restricted_ip: IPAddress):
#         self.user_id = user_id
#         self.restricted_ip = restricted_ip
#
#     def check(self, user: User, ip_dest: IPAddress) -> bool:
#         return user.id == self.user_id and self.restricted_ip.is_in_subnet(ip_dest.ip)
