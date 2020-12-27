from authx.authenticate import authenticator
from authx.authorizer import authorizer
from authx.exception import (InvalidPassword, InvalidUsername,
                             NotLoggedInError, NotPermittedError)

authenticator.add_user('joe', 'joepassword')
authorizer.add_permission('test program')
authorizer.add_permission('change program')
authorizer.permit_user('test program', 'joe')


class Editor:
    def __init__(self):
        self.username = None
        self.menu_map = {
            "login": self.login,
            "test": self.test,
            "change": self.change,
            "quit": self.quit
        }

    def is_permitted(self, permission):
        try:
            authorizer.check_permission(permission, self.username)
        except NotLoggedInError as e:
            print("{} is not logged int".format(e.username))
            return False
        except NotPermittedError as e:
            print("{} cannot {}".format(e.username, permission))
            return False
        else:
            return True

    def login(self):
        logged_in = False

        while not logged_in:
            username = input("username: ")
            password = input("password: ")

            try:
                logged_in = authenticator.login(username, password)
            except InvalidUsername:
                print("Sorry, that username does not exists")
            except InvalidPassword:
                print("Sorry, incorrect password")
            else:
                self.username = username
                print("Login successful!")

    def test(self):
        if self.is_permitted("test program"):
            print("Testing program now...")

    def change(self):
        if self.is_permitted("change program"):
            print("Changing program now...")

    def quit(self):
        raise SystemExit()

    def menu(self):
        print('Welcome to Auth Module!')
        try:
            answer = ""
            while True:
                print("""
                Please enter a command:
                \tlogin\tLogin
                \ttest\tTest the program
                \tchange\tChange the program
                \tquit\tQuit
                """)

                answer = input("enter a command: ").lower()

                try:
                    func = self.menu_map[answer]
                except KeyError:
                    print(f'{answer} is not a valid option')
                else:
                    func()
        finally:
            print("Thank you for testing the auth module")


if __name__ == '__main__':
    editor = Editor()
    editor.menu()
