import getpass

class Auth:
    def __init__(self):

        self.username = input("Username: ")
        self.password = getpass.getpass("Password: ")

    def get(self):
        return self.username, self.password