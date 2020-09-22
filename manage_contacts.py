import inquirer
import re
from contact import Contact
from file import File

class ManageContacts: #subclass of contact??

    @classmethod
    def email_validation(cls, answers, current):
        if not re.match('^[a-z0-9]+[\._-]?[a-z0-9]+[@]\w+[.]\w{2,3}[\.]?(\w{2,3})?$', current):
            inquirer.ValidationError('', reason='Invalid email format.')
        return True
    @classmethod
    def phone_validation(cls, answers, current): # how to account for international nums??
        if not current.isnumeric() or not re.match('(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', current):
            inquirer.ValidationError('', reason='Invalid phone number.')
        return True

    def add_contact(self, contacts_list: dict, groups_list: list) -> None:
        contact_info = inquirer.prompt([inquirer.Text(name='firstname', message='New contact first name'), inquirer.Text(name='lastname', message='New contact last name'), inquirer.Text(name='email', message='{firstname} {lastname} email', validate=ManageContacts.email_validation), inquirer.Text(name='phone', message='{firstname} {lastname} phone number', validate=ManageContacts.phone_validation), inquirer.Checkbox(name='groups', message='Select groups for {firstname} {lastname}', choices=[group for group in groups_list], default=[])])

        new_contact = Contact(**contact_info)
        new_contact.format_data(contacts_list)

    # classmethod??
    def select_contact(self, contacts_list: dict) -> dict:
        choice = inquirer.prompt([inquirer.List('selected', message='Select Contact', choices=contacts_list.keys())])
        return contacts_list[choice['selected']]

    # get contact from select_contact function
    def edit_contact(self, contact: dict, contacts_list: dict) -> None:
        edit = inquirer.prompt([inquirer.List('field', message='Choose field to edit', choices=['name', 'email', 'phone'])])

        if edit['field'] == 'name':
            edit = inquirer.prompt([inquirer.Text('firstname', message='Enter firstname'), inquirer.Text('lastname', message='Enter lastname')])
            new_name = edit['firstname'].capitalize() + " " + edit['lastname'].capitalize()
            contacts_list[new_name] = contacts_list.pop(contact['name'])
            contacts_list[new_name]['name'] = new_name
        elif edit['field'] == 'email':
            edit = inquirer.prompt([inquirer.Text('email', message='Enter email', validate=ManageContacts.email_validation)])
            new_data = edit['email']
            contacts_list[contact['name']]['email'] = edit['email']
        elif edit['field'] == 'phone':
            edit = inquirer.prompt([inquirer.Text('phone', message='Enter phone number', validate=ManageContacts.phone_validation)])
            new_data = edit['phone']
            contacts_list[contact['name']]['phone'] = edit['phone']

    def view_individual_contact(self, contact):
        print(f"Name: {contact['name']}\nEmail: {contact['email']}\nPhone: {contact['phone']}\nGroups: {contact['groups']}")

    def view_all_contacts(self, contacts_list):
        print(f"{'Name:':25}{'Email:':35}{'Phone:':20}{'Groups:':20}")
        for contact, details in contacts_list.items():
            print(f"{details['name']:25}{details['email']:35}{details['phone']:20}{details['groups']}")



contact = ManageContacts()
# contacts_list = File.load_data('client.json')
groups = ['family', 'friends', 'coworkers']
load_file = File.load_data('client.json')
# print(load_file)
user = {'password': 'fool', 'contacts': {}}
user['contacts'] = load_file
print(user)
contacts_list = user['contacts']

# contact.add_contact(contacts_list, groups)
File.save_to_file('client.json', contacts_list)
contact.select_contact(contacts_list)
contact.edit_contact(contact.select_contact(contacts_list), contacts_list)
contact.view_all_contacts(contacts_list)
# print(contacts_list)
