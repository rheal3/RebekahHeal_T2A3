from user import User
from file import File

file_path = '.client.json'
user_data = File.load_data(file_path)
current_user = User.user_menu(user_data, file_path)

contacts_dict = user_data[current_user]['contacts']

groups_list = user_data[current_user]['groups_dict'].keys()
groups_dict = user_data[current_user]['groups_dict']

User.main_menu(user_data, contacts_dict, groups_dict, file_path, current_user)
