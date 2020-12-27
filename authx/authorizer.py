from authx.authenticate import authenticator
from authx.exception import (InvalidUsername, NotLoggedInError,
                             NotPermittedError, PermissionError)


class Authorizer:
    def __init__(self, authenticator):
        self.authenticator = authenticator
        self.permissions = {}

    def add_permission(self, perm_name):
        """
        Create a new permission that users can be added to
        """
        try:
            perm_set = self.permissions[perm_name]
        except KeyError:
            self.permissions[perm_name] = set()
        else:
            raise PermissionError("Permission Exists")

    def permit_user(self, perm_name, username):
        """
        Grant the given permission to the user
        """
        try:
            perm_set = self.permissions[perm_name]
        except KeyError:
            raise PermissionError("Permission does not exists!")
        else:
            if username not in self.authenticator.users:
                raise InvalidUsername(username)
            perm_set.add(username)

    def check_permission(self, perm_name, username):
        """
        Checks whether a user has a specific permission or not. 

        In order to evaluate if a permission is granted a user

        - needs to be logged in
        - be in the set of users tied to a `perm_name`

        else an exception is raised.
        """
        if not self.authenticator.is_logged_in(username):
            raise NotLoggedInError(username)

        try:
            perm_set = self.permissions[perm_name]
        except KeyError:
            raise PermissionError("Permission does not exist")
        else:
            if not username in perm_set:
                return NotPermittedError(username)
            else:
                return True


authorizer = Authorizer(authenticator)
