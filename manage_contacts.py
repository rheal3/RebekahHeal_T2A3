import inquirer
import re
from contact import Contact
from file import File

class ManageContacts: #subclass of contact??

    def add_contact(self, contacts_list: dict, groups_list: list) -> None:
        # validate non entry?? blank fields?
        def email_validation(answers, current):
            if not re.match('^[a-z0-9]+[\._-]?[a-z0-9]+[@]\w+[.]\w{2,3}[\.]?(\w{2,3})?$', current):
                inquirer.ValidationError('', reason='Invalid email format.')
            return True

        def phone_validation(answers, current): # how to account for international nums??
            if not current.isnumeric() or not re.match('(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', current):
                inquirer.ValidationError('', reason='Invalid phone number.')
            return True

        contact_info = [inquirer.Text(name='firstname', message='New contact first name'), inquirer.Text(name='lastname', message='New contact last name'), inquirer.Text(name='email', message='{firstname} {lastname} email', validate=email_validation), inquirer.Text(name='phone', message='{firstname} {lastname} phone number', validate=phone_validation), inquirer.Checkbox(name='groups', message='Select groups for {firstname} {lastname}', choices=[group for group in groups_list], default=[])]

        contact_info = inquirer.prompt(contact_info)

        new_contact = Contact(**contact_info)
        new_contact.format_data(contacts_list)

    # classmethod??
    def select_contact(self, contacts_list: dict) -> dict:
        choice = [inquirer.List('selected', message='Select Contact', choices=contacts_list.keys())]
        choice = inquirer.prompt(choice)
        return contacts_list[choice['selected']]

    def edit_contact(self, contact, contacts_list):
        edit = [inquirer.List('field', message='Choose field to edit', choices=contact.keys())]
        edit = inquirer.prompt(edit)
        # can you put a function in inquirer to return specific field to edit? if edit['field'] == 'name' then ...

contact = ManageContacts()
contacts_list = File.load_data('client.txt')
groups = ['family', 'friends', 'coworkers']
# contact.add_contact(contacts, groups)
# File.save_to_file('client.txt', contacts_list)
# contact.select_contact(contacts_list)
contact.edit_contact(contact.select_contact(contacts_list), contacts_list)
