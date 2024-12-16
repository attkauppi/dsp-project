class MessageManager:
    def __init__(self):
        self.connected_clients = {}  # Store {username: conn} for TCP

    def broadcast_message(self, username, message, online_users):
        if username not in online_users:
            return b"User not logged in."

        full_message = f"{username}: {message}"
        for user, conn in self.connected_clients.items():
            if user != username:  # Don't send the message to the sender
                try:
                    conn.send(full_message.encode('utf-8'))
                except Exception as e:
                    print(f"Error sending to {user}: {e}")
        return b"Message broadcasted."