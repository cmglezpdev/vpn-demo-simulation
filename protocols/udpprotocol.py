import socket
import struct


class UDPProtocol:
    """
    This class represents a UDP Protocol object. It has methods for sending and receiving UDP packets.

    Attributes:
        ip (str): The IP address for the UDP protocol.
        port (int): The port number for the UDP protocol.
    """
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)

        self._socket.bind((self.ip, self.port))
        self._socket.setblocking(False)
        self._stop = True

    def send(self, data: str, dip: str, dport: int):
        """
        Sends a UDP packet.

        Parameters:
            data (str): The data to be sent.
            dip (str): The destination IP address.
            dport (int): The destination port number.
        """
        data = data.encode('utf-8')
        length = len(data) + 8

        udp_data = struct.pack('!HHHH', self.port, dport, length, 0) + data
        checksum = self.__calculate_checksum(self.ip, dip, udp_data)
        udp_header = struct.pack('!HHHH', self.port, dport, length, checksum)

        self._socket.sendto(udp_header + data, (dip, dport))
        print(f"UDP: {data} sent to {dip}:{dport}")

    @staticmethod
    def __calculate_checksum(sip: str, dip: str, data: bytes):
        """
        Calculates the checksum for a UDP packet.

        Parameters:
           sip (str): The source IP address.
           dip (str): The destination IP address.
           data (bytes): The data for the UDP packet.

        Returns:
           int: The calculated checksum.
        """
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
        """
        Starts the UDP protocol.
        """
        self._stop = False
        while not self._stop:
            try:
                wrong = False
                data, addr = self._socket.recvfrom(1024)
                print(data)

                header = struct.unpack('!HHHH', data[20:28])
                [sport, dport, length, checksum] = header

                if dport != self.port:
                    continue

                sender_ip, _ = addr
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
        """
        Closes the UDP protocol.
        """
        self._stop = True
        self._socket.close()
