import socket
from protocol import Protocol
from scapy.all import IP, UDP, send

class UDPProtocol():
    def __init__(self, ip, port):
      self.ip = ip
      self.port = port
      self.stop = False
      self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)

      self.socket.bind(self.ip, self.port)
      self.socket.setblocking(False)

    def send(self, data, dest_ip, dest_port):
      udp_packet = IP(dst=dest_ip)/UDP(dport=dest_port)/data
      self.socket.send(udp_packet)

    def start(self):
        while not self.stop:
            try:
                data, src_addr = self.socket.recvfrom(1024)
                packet = IP(data)
                
                if UDP in packet:
                    udp_packet = packet[UDP]

                    if udp_packet.dport != self._port:
                        continue

                    sender_ip = src_addr[0]
                    print(f'UDP data received from {sender_ip}:{udp_packet.dport}')

                    if udp_packet.chksum != 0:
                        if UDP.verify_chksum(packet):
                            data = udp_packet.payload.decode('utf-8')
                            print(f'Data: {data}')
                            print(f'Length: {len(data)}, Checksum: {udp_packet.chksum}\n')
                        else:
                            print('Corrupted data\n')
                        yield data

            except BlockingIOError:
                continue

    def stop(self):
        self.__stop = True
        self.__s.close()