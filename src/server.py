import socket
import threading
from user_manager import UserManager
from message_manager import MessageManager
from constants import TCP_PORT, BUFFER_SIZE, UDP_PORT
import struct

class P2PServer:
    def __init__(self):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_socket.bind(("", TCP_PORT))
        self.tcp_socket.listen(5)

        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.udp_socket.bind(("", UDP_PORT))

        self.user_manager = UserManager()
        self.message_manager = MessageManager()

        print(f"Server started on TCP port {TCP_PORT} and UDP port {UDP_PORT}")

    def handle_tcp_client(self, conn, addr):
        username = None
        try:
            while True:
                packet = conn.recv(BUFFER_SIZE)
                if not packet:
                    break

                code, username_bytes, password_or_message_bytes = struct.unpack('b 20s 100s', packet)
                username = username_bytes.decode('utf-8').strip('\x00')
                password_or_message = password_or_message_bytes.decode('utf-8').strip('\x00')

                if code == 0:
                    response = self.user_manager.register_user(username, password_or_message)
                elif code == 1:
                    response = self.user_manager.login_user(username, password_or_message, addr)
                    if response == b"Login successful.":
                        self.message_manager.connected_clients[username] = conn
                elif code == 2:
                    response = self.message_manager.broadcast_message(username, password_or_message, self.user_manager.online_users)
                elif code == 3:
                    response = self.user_manager.logout_user(username)
                    if username in self.message_manager.connected_clients:
                        del self.message_manager.connected_clients[username]
                else:
                    response = b"Invalid Request"

                conn.send(response)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if username and username in self.message_manager.connected_clients:
                del self.message_manager.connected_clients[username]
            conn.close()

    def handle_udp(self):
        while True:
            packet, addr = self.udp_socket.recvfrom(BUFFER_SIZE)
            print(f"UDP Message from {addr}: {packet.decode('utf-8')}")

    def start(self):
        threading.Thread(target=self.handle_udp, daemon=True).start()
        while True:
            conn, addr = self.tcp_socket.accept()
            print(f"New TCP connection from {addr}")
            threading.Thread(target=self.handle_tcp_client, args=(conn, addr), daemon=True).start()
