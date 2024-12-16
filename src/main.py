from server import P2PServer
from client import P2PClient

if __name__ == "__main__":
    mode = input("Start as server or client? (s/c): ").lower()
    if mode == 's':
        server = P2PServer()
        server.start()
    elif mode == 'c':
        server_ip = input("Enter server IP: ")
        client = P2PClient(server_ip)
        client.connect()
        client.start()