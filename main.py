import threading

from protocols import UDPProtocol
from vpnserver import VPNServer


class Main:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.protocol = UDPProtocol(ip, port)
        self.vpn = VPNServer(self.protocol)
        self.vpn_thread = None

    def __help_menu(self):
        print("\n===== Help Menu =====")
        print("\n==Menu commands==")
        print("1. help: Show this menu")
        print("2. exit: Exit the program")
        print("\n== VPN commands ==")
        print("1. start PROTOCOL: Start the vpn server")
        print("2. create_user USERNAME PASSWORD ID_VLAN: Create a new user in a VLAN")
        print("3. list_users [VLAN_ID]: List all users or users in a VLAN")
        print("4. stop: Stop the vpn server")
        print("\n== Firewall commands ==")
        print("1. restrict_vlan ID_VLAN IP_NETWORK: Restrict a vlan to a network")
        print("2. restrict_user ID_USER IP_NETWORK: Restrict a user to a network")
        print("\n")

    def start(self):
        print("Welcome to VPN Server")
        print(f"VPN running on {self.ip}:{self.port}")
        self.__help_menu()

        while True:
            command = input("Enter Command: ").split(" ")

            if len(command) == 0:
                print("Invalid command")

            [cmd, *args] = command

            if cmd == "start" and len(args) == 0:
                if self.vpn_thread is not None:
                    print("VPN already started")
                    continue

                self.vpn_thread = threading.Thread(target=self.vpn.start)
                self.vpn_thread.start()

            elif cmd == "stop" and len(args) == 0:
                if self.vpn_thread is None:
                    print("VPN is stopped")
                    continue

                self.vpn.stop()
                self.vpn_thread.join()
                self.vpn_thread = None

            elif cmd == "create_user" and len(args) == 3 and args[2].isdigit():
                self.vpn.create_user(args[0], args[1], int(args[2]))

            elif cmd == "remove_user" and len(args) == 1:
                self.vpn.remove_user(args[0])

            elif cmd == "list_users" and (len(args) == 0 or len(args) == 1 and args[0].isdigit()):
                vlan_id = int(args[0]) if len(args) == 1 else None
                self.vpn.list_users(vlan_id)

            elif cmd == "help" and len(args) == 0:
                self.__help_menu()

            elif cmd == "exit" and len(args) == 0:
                if self.vpn_thread is not None:
                    self.vpn.stop()
                    self.vpn_thread.join()
                    self.vpn_thread = None
                break

            else:
                print("Invalid command")


main = Main("127.0.0.1", 3001)

main.start()
