import socket
import struct


class UDPProtocol:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)

        self.socket.bind((self.ip, self.port))
        self.socket.setblocking(False)
        self.stop = True

    def send(self, data: str, dip: str, dport: int):
        data = data.encode('utf-8')
        length = len(data) + 8

        udp_data = struct.pack('!HHHH', self.port, dport, length, 0) + data
        checksum = self.__calculate_checksum(self.ip, dip, udp_data)
        udp_header = struct.pack('!HHHH', self.port, dport, length, checksum)

        self.socket.sendto(udp_header + data, (dip, dport))
        print(f"UDP: {data} sent to {dip}:{dport}")

    @staticmethod
    def __calculate_checksum(sip: str, dip: str, data: bytes):
        sip = socket.inet_aton(sip)
        dip = socket.inet_aton(dip)

        packet = struct.pack('!4s4sHH', sip, dip, len(data), 0) + data

        checksum = 0
        for i in range(0, len(packet), 2):
            checksum += (packet[i] if i + 1 >= len(packet) else (packet[i] << 8) + (packet[i + 1]))

            while checksum >> 16:
                checksum = (checksum & 0xffff) + (checksum >> 16)

        checksum = ~checksum & 0xffff

        return checksum

    def start(self):
        self.stop = False
        while not self.stop:
            try:
                wrong = False
                data, addr = self.socket.recvfrom(1024)

                header = struct.unpack('!HHHH', data[20:28])
                [sport, dport, length, checksum] = header

                if dport != self.port:
                    continue

                sender_ip = addr[0]
                zero_checksum_header = (data[20:28])[:6] + b'\x00\x00' + (data[20:28])[8:]
                calculated_checksum = self.__calculate_checksum(sender_ip, self.ip, zero_checksum_header + data[28:])

                print(f"UDP data received from {sender_ip}:{sport}")

                if calculated_checksum == checksum:
                    data = data[28:].decode('utf-8')
                    print(f"UDP Data: {data}")
                    print(f"UDP Length: {length}")
                    print(f"UDP Checksum: {checksum}")
                else:
                    wrong = True
                    print("UDP: Invalid checksum")

                if not wrong:
                    yield data

            except BlockingIOError:
                continue

    def close(self):
        self.stop = True
        self.socket.close()
