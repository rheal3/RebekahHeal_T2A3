from file import File
from manage_contacts import ManageContacts
from groups import Groups
from follow_up import FollowUp
import inquirer
import os
import bcrypt


class User:
    user_options = ["Login", "Create User"]

    @classmethod
    def user_menu(cls, user_data, file_path):
        os.system('clear')
        if len(user_data) > 0:
            options = inquirer.prompt([inquirer.List('choice',
                                      message="WELCOME TO THE APP!!!",
                                      choices=cls.user_options)])
            if options['choice'] == 'Login':
                user = cls.login(user_data)
                return user
            elif options['choice'] == 'Create User':
                cls.create_user(user_data)
                File.save_to_file(file_path, user_data)
                user = cls.user_menu(user_data, file_path)
                return user
        else:
            options = inquirer.prompt([inquirer.List('choice',
                                      message="WELCOME TO THE APP!!!",
                                      choices=['Create User'])])
            cls.create_user(user_data)
            File.save_to_file(file_path, user_data)
            user = cls.user_menu(user_data, file_path)
            return user

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf8'),
                             bcrypt.gensalt()).decode('utf8')

    @classmethod
    def login(cls, user_data):
        def username_validation(answers, current):
            if not user_data.get(current, False):
                message = "Invalid username."
                raise inquirer.errors.ValidationError('', reason=message)
            return True

        user = inquirer.prompt([inquirer.Text('username',
                               message="Enter username",
                               validate=username_validation)])
        password = inquirer.prompt([inquirer.Password('password',
                                   message="Enter Password")])
        while not bcrypt.checkpw(password['password'].encode('utf8'),
                                 user_data[user['username']]['password'].
                                 encode('utf8')):
            print("Incorrect password.")
            password = inquirer.prompt([inquirer.Password('password',
                                       message="Enter Password")])
        return user['username']

    @classmethod
    def create_user(cls, user_data):
        def username_validation(answers, current):
            if user_data.get(current, False):
                message = "Username already in use."
                raise inquirer.errors.ValidationError('', reason=message)
            current = current.lower()
            return True

        def password_validation(answers, current):
            if current != answers['initial_password']:
                message = "Passwords do not match."
                raise inquirer.errors.ValidationError('', reason=message)
            return True

        username = inquirer.Text('username', message="Enter Username",
                                 validate=username_validation)
        initial = inquirer.Password('initial_password',
                                    message="Enter Password")
        verify = inquirer.Password('password', message="Re-Enter Password",
                                   validate=password_validation)

        new_user = inquirer.prompt([username, initial, verify])

        password = cls.hash_password(new_user['password'])
        user_data[new_user['username']] = {'password': password,
                                           'contacts': {}, 'groups_dict': {}}

    @staticmethod
    def main_menu(user_data, contacts_dict, groups_dict, file_path,
                  current_user):
        os.system('clear')
        if len(contacts_dict) > 0:
            options = inquirer.prompt([inquirer.List('choice',
                                      message='Choose Option',
                                      choices=['Manage Contacts',
                                               'Manage Groups', 'Follow Up',
                                               'Logout'])])
        else:
            ManageContacts.manage_contacts_menu(user_data, contacts_dict,
                                                groups_dict, file_path,
                                                current_user)

        if options['choice'] == 'Manage Contacts':
            os.system('clear')
            ManageContacts.manage_contacts_menu(user_data, contacts_dict,
                                                groups_dict, file_path,
                                                current_user)
        elif options['choice'] == 'Manage Groups':
            os.system('clear')
            Groups.groups_menu(user_data, groups_dict, file_path,
                               contacts_dict, current_user)
        elif options['choice'] == 'Follow Up':
            os.system('clear')
            FollowUp.follow_up_menu(contacts_dict, current_user, user_data,
                                    groups_dict, file_path)
        elif options['choice'] == 'Logout':
            print("Goodbye.")
            exit()
