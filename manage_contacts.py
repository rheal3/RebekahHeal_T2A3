import inquirer
import re
from contact import Contact
from file import File

class ManageContacts: #subclass of contact??

    def add_contact(self, contact_list: list, groups_list: list) -> None:
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
        new_contact.format_data(contact_list)

    def select_contact(self, contacts_list):
        pass

# groups = ['family', 'friends', 'colleuges', 'boss', 'animals'] # get groups from Groups Class
# user_data = File.load_data('client.txt')
# user_data['contacts'] = []

# ezra = ManageContacts()
# ezra.add_contact(user_data['contacts'], groups)
#
# File.save_to_file('client.txt', user_data)
#
# print(user_data)
# print(ezra.format_contacts(user_data['contacts']))
# ezra.select_contact(user_data['contacts'])
