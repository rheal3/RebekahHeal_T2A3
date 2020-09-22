from user import User
from file import File
from manage_contacts import ManageContacts
import inquirer #take away later

file_path = 'client.json'
user_data = File.load_data(file_path)
current_user = User.user_menu(user_data)

contacts_list = user_data[current_user]['contacts']

groups = ['family', 'friends', 'colleuges', 'other'] # import from groups function

ManageContacts.manage_contacts_menu(user_data, contacts_list, groups, file_path)
