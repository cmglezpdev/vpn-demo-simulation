import socket
from protocol import Protocol

class UDPProtocol(Protocol):
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.server_socket.bind((self.host, self.port))
    print(f"Server listening on {self.host}:{self.port}")

  def send(self, data):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(data.encode(), (self.host, self.port))
    client_socket.close()

  def receive(self):
    data, addr = self.server_socket.recvfrom(1024)
    return data.decode()
  
  def close(self):
    self.server_socker.close()

  

## Example of use
# host = '1027.0.0.1'
# port = 12345

# server = UPDProtocol(host, port)

# while True:
#   try:
#     data = server.receive()

#     print(f"Received: {data}")

#     response = "Hello client! I recieved your message."
#     server.send(response)
#   except KeyboardInterrupt:
#     print("Closing server...")
#     server.close()
#     break
  