from file import File
import inquirer

class User:
    user_options = ["Login", "Create User"]

    @staticmethod
    def user_menu(user_data, file_path):
        #clear screen
        if len(user_data) > 0:
            options = inquirer.prompt([inquirer.List('choice', message="WELCOME TO THE APP!!!", choices=User.user_options)])
            if options['choice'] == 'Login':
                user = User.login(user_data)
                return user
            elif options['choice'] == 'Create User':
                User.create_user(user_data)
                File.save_to_file(file_path, user_data)
                user = User.user_menu(user_data, file_path)
                return user
        else:
            options = inquirer.prompt([inquirer.List('choice', message="WELCOME TO THE APP!!!", choices=['Create User'])])
            User.create_user(user_data)
            File.save_to_file(file_path, user_data)
            user = User.user_menu(user_data, file_path)
            return user

    @classmethod
    def login(cls, user_data):
        def username_validation(answers, current):
            if not user_data.get(current, False):
                raise errors.ValidationError('', reason="Invalid username.")
            return True
        def password_validation(answers, current):
            if current != user_data[answers['username']]['password']:
                raise errors.ValidationError('', reason="Incorrect password.")
            return True

        user = inquirer.prompt([inquirer.Text('username', message="Enter username", validate=username_validation), inquirer.Password('password', message="Enter Password", validate=password_validation)])
        return user['username']

    @classmethod
    def create_user(cls, user_data):
        def username_validation(answers, current):
            if user_data.get(current, False):
                raise errors.ValidationError('', reason="Username already in use.")
            current = current.lower()
            return True

        def password_validation(answers, current):
            if current != answers['initial_password']:
                raise errors.ValidationError('', reason="Passwords do not match.")
            return True

        new_user = inquirer.prompt([inquirer.Text('username', message="Enter Username", validate=username_validation), inquirer.Password('initial_password', message="Enter Password"), inquirer.Password('validated_password', message="Re-Enter Password", validate=password_validation)])

        user_data[new_user['username'].lower()] = {'password': new_user['validated_password'], 'contacts': {}, 'groups_dict': {}}


# user_data = File.load_data('client.json')
# current_user = User.user_menu(user_data)
