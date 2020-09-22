import inquirer
import re
from contact import Contact
from file import File
# from groups import Groups


class ManageContacts: #subclass of contact??
    manage_contacts_options = ['Add Contact', 'Edit Contact', 'View Contact', 'View All Contacts', 'Logout']

    @staticmethod
    def manage_contacts_menu(user_data, contacts_dict, groups_dict, file_path):
        if len(contacts_dict) > 0:
            options = inquirer.prompt([inquirer.List('choice', message="Select Option", choices=ManageContacts.manage_contacts_options)])
        else:
            options = inquirer.prompt([inquirer.List('choice', message="Select Option", choices=['Add Contact', 'Logout'])])
        if options['choice'] == 'Add Contact':
            ManageContacts.add_contact(contacts_dict, groups_dict)
            File.save_to_file(file_path, user_data)
        elif options['choice'] == 'Edit Contact':
            ManageContacts.edit_contact(ManageContacts.select_contact(contacts_dict), contacts_dict, groups_dict)
            File.save_to_file(file_path, user_data)
        elif options['choice'] == 'View Contact':
            ManageContacts.view_individual_contact(ManageContacts.select_contact(contacts_dict))
            input("Press Enter to Continue")
        elif options['choice'] == 'View All Contacts':
            ManageContacts.view_all_contacts(contacts_dict)
            input("Press Enter to Continue")
        elif options['choice'] == 'Logout':
            print("Goodbye.")
            exit()
        # add screen clear
        ManageContacts.manage_contacts_menu(user_data, contacts_dict, groups_dict, file_path)

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

    @classmethod
    def add_contact(cls, contacts_dict: dict, groups_dict: dict) -> None:
        contact_info = inquirer.prompt([inquirer.Text(name='firstname', message='New contact first name'), inquirer.Text(name='lastname', message='New contact last name'), inquirer.Text(name='email', message='{firstname} {lastname} email', validate=ManageContacts.email_validation), inquirer.Text(name='phone', message='{firstname} {lastname} phone number', validate=ManageContacts.phone_validation), inquirer.Checkbox(name='groups', message='Select groups for {firstname} {lastname}', choices=[group for group in groups_dict.keys()], default=[])])

        new_contact = Contact(**contact_info).format_data(contacts_dict)

    @classmethod
    def select_contact(cls, contacts_dict: dict) -> dict:
        choice = inquirer.prompt([inquirer.List('selected', message='Select Contact', choices=contacts_dict.keys())])
        return contacts_dict[choice['selected']]

    # get contact from select_contact function
    @classmethod
    def edit_contact(self, contact: dict, contacts_dict: dict, groups_dict: dict) -> None:
        if len(groups_dict) > 0:
            edit = inquirer.prompt([inquirer.List('field', message='Choose field to edit', choices=['name', 'email', 'phone', 'groups'])])
        else:
            edit = inquirer.prompt([inquirer.List('field', message='Choose field to edit', choices=['name', 'email', 'phone'])])

        if edit['field'] == 'name':
            edit = inquirer.prompt([inquirer.Text('firstname', message='Enter new firstname'), inquirer.Text('lastname', message='Enter new lastname')])
            new_name = edit['firstname'].capitalize() + " " + edit['lastname'].capitalize()
            contacts_dict[new_name] = contacts_dict.pop(contact['name'])
            contacts_dict[new_name]['name'] = new_name
        elif edit['field'] == 'email':
            edit = inquirer.prompt([inquirer.Text('email', message='Enter new email', validate=ManageContacts.email_validation)])
            contacts_dict[contact['name']]['email'] = edit['email']
        elif edit['field'] == 'phone':
            edit = inquirer.prompt([inquirer.Text('phone', message='Enter new phone number', validate=ManageContacts.phone_validation)])
            contacts_dict[contact['name']]['phone'] = edit['phone']
        elif edit['field'] == 'groups':
            edit = inquirer.prompt([inquirer.Checkbox('groups', message='Choose groups', choices=groups_dict.keys())])
            contacts_dict[contact['name']]['groups'] = [edit['groups']]

    @classmethod
    def view_individual_contact(self, contact):
        print(f"Name: {contact['name']}\nEmail: {contact['email']}\nPhone: {contact['phone']}\nGroups: {contact['groups']}")

    @classmethod
    def view_all_contacts(self, contacts_dict):
        print(f"{'Name:':25}{'Email:':35}{'Phone:':20}{'Groups:':20}")
        for contact, details in contacts_dict.items():
            print(f"{details['name']:25}{details['email']:35}{details['phone']:20}{details['groups']}")
