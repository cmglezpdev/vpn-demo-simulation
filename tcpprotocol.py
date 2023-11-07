import socket
from protocol import Protocol

class TCPProtocol(Protocol):
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server_socket.bind(self.host, self.port)
    self.server_socket.listen(1)
    print(f"Server listening on {self.host}:{self.port}")

  def send(self, data):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((self.host, self.port))
    client_socket.sendall(data.encode())
    client_socket.close()

  def receive(self):
    client_socket, addr = self.server_socket.accept()
    data = client_socket.recv(1024).decode()
    client_socket.close()
    return data

  def close(self):
    self.socket.close()


## Example of use
# host = '1027.0.0.1'
# port = 12345

# server = TCPProtocol(host, port)

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
  