import time

class UserManager:
    def __init__(self):
        self.db = {}
        self.online_users = {}

    def register_user(self, username, password):
        if username in self.db:
            return b"User already exists."
        self.db[username] = password
        return b"Registration successful."

    def login_user(self, username, password, addr):
        if username in self.online_users:
            return b"User already logged in."
        if username in self.db and self.db[username] == password:
            self.online_users[username] = (addr[0], time.time())
            return b"Login successful."
        return b"Invalid credentials."

    def logout_user(self, username):
        if username in self.online_users:
            del self.online_users[username]
            return b"Logout successful."
        return b"User not logged in."