import socket
import struct
import threading
from constants import TCP_PORT, BUFFER_SIZE

class P2PClient:
    def __init__(self, server_ip):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = server_ip
        self.username = None

    def connect(self):
        self.tcp_socket.connect((self.server_ip, TCP_PORT))

    def send_tcp(self, code, username, password_or_message):
        packet = struct.pack('b 20s 100s', code, username.encode('utf-8'), password_or_message.encode('utf-8'))
        self.tcp_socket.send(packet)
        response = self.tcp_socket.recv(BUFFER_SIZE).decode('utf-8')
        print(f"Server Response: {response}")
    
    def send_message(self, message):
        if not self.username:
            print("Login first!")
            return
        self.send_tcp(2, self.username, message)

    def listen_for_messages(self):
        while True:
            try:
                message = self.tcp_socket.recv(BUFFER_SIZE).decode('utf-8')
                if message:
                    print(f"\n{message}")
            except Exception as e:
                print(f"Disconnected from server: {e}")
                break

    def register(self, username, password):
        self.send_tcp(0, username, password)

    def login(self, username, password):
        self.username = username
        self.send_tcp(1, username, password)

    def logout(self):
        if not self.username:
            print("Login first!")
            return
        self.send_tcp(3, self.username, "")

    def start(self):
        threading.Thread(target=self.listen_for_messages, daemon=True).start()
        while True:
            print("\n1. Register\n2. Login\n3. Send Message\n4. Logout\n5. Exit")
            choice = int(input("Enter your choice: "))
            if choice == 1:
                username = input("Enter username: ")
                password = input("Enter password: ")
                self.register(username, password)
            elif choice == 2:
                username = input("Enter username: ")
                password = input("Enter password: ")
                self.login(username, password)
            elif choice == 3:
                message = input("Enter message: ")
                self.send_message(message)
            elif choice == 4:
                self.logout()
            elif choice == 5:
                break
