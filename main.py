from user import User
from file import File
from manage_contacts import ManageContacts
import inquirer #take away later?

file_path = 'client.json'
user_data = File.load_data(file_path)
current_user = User.user_menu(user_data, file_path)

contacts_dict = user_data[current_user]['contacts']

groups_list = user_data[current_user]['groups_dict'].keys() # import from groups function
groups_dict = user_data[current_user]['groups_dict']



User.main_menu(user_data, contacts_dict, groups_dict, file_path, current_user)
