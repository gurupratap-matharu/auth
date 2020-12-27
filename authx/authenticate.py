from authx.exception import (InvalidPassword, InvalidUsername,
                             PasswordTooShort, UsernameAlreadyExists)
from authx.user import User


class Authenticator:
    def __init__(self):
        """
        Construct an authenticator to manage users logging and out.
        """
        self.users = {}

    def add_user(self, username, password):
        if username in self.users:
            raise UsernameAlreadyExists(username)
        if len(password) < 6:
            raise PasswordTooShort(username)
        self.users[username] = User(username, password)

    def login(self, username, password):
        """
        Logs in a user if valid username and password are provided
        Else raises elegant exceptions.

        Finally returns a boolean
        """
        try:
            user = self.users[username]
        except KeyError:
            raise InvalidUsername(username)

        if not user.check_password(password):
            raise InvalidPassword(username, user)

        user.is_logged_in = True
        return True

    def is_logged_in(self, username):
        """
        Determines if a user is already logged into the system.
        Doesn't raise any exception incase we don't find the user.
        Simply returns a boolean.
        """
        if username in self.users:
            return self.users[username].is_logged_in
        return False


authenticator = Authenticator()
