from protocols import UDPProtocol

protocol = UDPProtocol('127.0.0.1', 3002)

print('Server UDP started')
for data in protocol.start():
    print(f"Data received: {data}")
