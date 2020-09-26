import inquirer
import re
from contact import Contact
from file import File
import os


class ManageContacts:
    manage_contacts_options = ['Add Contact', 'Edit Contact', 'View Contact',
                               'View All Contacts', 'Go Back']

    @classmethod
    def manage_contacts_menu(cls, user_data, contacts_dict, groups_dict,
                             file_path, current_user):
        os.system('clear')
        if len(contacts_dict) > 0:
            options = inquirer.prompt([inquirer.List('choice',
                                      message="Select Option",
                                      choices=cls.manage_contacts_options)])
        else:
            options = inquirer.prompt([inquirer.List('choice',
                                      message="Select Option",
                                      choices=['Add Contact', 'Logout'])])

        os.system('clear')
        if options['choice'] == 'Add Contact':
            cls.add_contact(contacts_dict, groups_dict)
            File.save_to_file(file_path, user_data)
        elif options['choice'] == 'Edit Contact':
            edit = cls.edit_contact(cls.select_contact(contacts_dict),
                                    contacts_dict, groups_dict)
            File.save_to_file(file_path, user_data)
            from follow_up import FollowUp
            FollowUp.set_dates(edit, groups_dict)

        elif options['choice'] == 'View Contact':
            cls.view_individual_contact(cls.select_contact(contacts_dict))
            input("Press Enter to Continue")
        elif options['choice'] == 'View All Contacts':
            cls.view_all_contacts(contacts_dict)
            input("Press Enter to Continue")
        elif options['choice'] == 'Go Back':
            from user import User
            User.main_menu(user_data, contacts_dict, groups_dict, file_path,
                           current_user)
        elif options['choice'] == 'Logout':
            print("Goodbye.")
            exit()

        cls.manage_contacts_menu(user_data, contacts_dict, groups_dict,
                                 file_path, current_user)

    @classmethod
    def email_validation(cls, answers, current):
        regex = '^[a-z0-9]+[\._-]?[a-z0-9]+[@]\w+[.]\w{2,3}[\.]?(\w{2,3})?$'
        if not re.match(regex, current):
            message = 'Invalid email format.'
            raise inquirer.errors.ValidationError('', reason=message)
        return True

    @classmethod
    def phone_validation(cls, answers, current):
        regex = '(\d{2}[\s]??\d{4}[-]??\d{4})'
        if not re.match(regex, current) or not current.isnumeric():
            message = 'Invalid phone number.'
            raise inquirer.errors.ValidationError('', reason=message)
        return True

    @classmethod
    def add_contact(cls, contacts_dict: dict, groups_dict: dict) -> None:
        firstname = inquirer.Text(name='firstname',
                                  message='New Contact First Name')
        lastname = inquirer.Text(name='lastname',
                                 message='New Contact Last Name')
        email = inquirer.Text(name='email',
                              message='New Contact Email',
                              validate=cls.email_validation)
        phone = inquirer.Text(name='phone',
                              message='New Contact Phone Number',
                              validate=cls.phone_validation)
        message = "Select groups \033[3m(select using > arrow key)\033[0m"
        groups = inquirer.Checkbox(name='groups',
                                   message=message,
                                   choices=[group for group in
                                            groups_dict.keys()],
                                   default=[])
        if len(groups_dict) > 0:
            contact_info = inquirer.prompt([firstname, lastname, email, phone,
                                            groups])
        else:
            contact_info = inquirer.prompt([firstname, lastname, email, phone])

        Contact(**contact_info).format_data(contacts_dict)

    @classmethod
    def select_contact(cls, contacts_dict: dict) -> dict:
        select = inquirer.List('selected', message='Select Contact',
                               choices=contacts_dict.keys())
        choice = inquirer.prompt([select])
        return contacts_dict[choice['selected']]

    # get contact from select_contact function
    @classmethod
    def edit_contact(cls, contact: dict, contacts_dict: dict,
                     groups_dict: dict) -> None:
        if len(groups_dict) > 0:
            field = inquirer.List('field', message='Choose field to edit',
                                  choices=['name', 'email', 'phone', 'groups',
                                           'Remove Contact'])
            edit = inquirer.prompt([field])
        else:
            field = inquirer.List('field', message='Choose field to edit',
                                  choices=['name', 'email', 'phone',
                                           'Remove Contact'])
            edit = inquirer.prompt([field])

        if edit['field'] == 'name':
            edit = inquirer.prompt([inquirer.Text('first',
                                   message='Enter New First Name'),
                                   inquirer.Text('last',
                                   message='Enter New Last Name')])
            new_name = (edit['first'] + " " + edit['last']).title()
            contacts_dict[new_name] = contacts_dict.pop(contact['name'])
            contacts_dict[new_name]['name'] = new_name
        elif edit['field'] == 'email':
            edit = inquirer.prompt([inquirer.Text('email',
                                   message='Enter New Email',
                                   validate=cls.email_validation)])
            contacts_dict[contact['name']]['email'] = edit['email']
        elif edit['field'] == 'phone':
            edit = inquirer.prompt([inquirer.Text('phone',
                                   message='Enter new phone number ##########',
                                   validate=cls.phone_validation)])
            contacts_dict[contact['name']]['phone'] = edit['phone']
        elif edit['field'] == 'groups':
            message = 'Choose groups \033[3m(select using > arrow key)\033[0m'
            edit = inquirer.prompt([inquirer.Checkbox('groups',
                                    message=message,
                                    choices=groups_dict.keys())])
            contacts_dict[contact['name']]['groups'] = edit['groups']
        elif edit['field'] == 'Remove Contact':
            check = inquirer.confirm("Are you sure you want to delete?",
                                     default=False)
            if check:
                del contacts_dict[contact['name']]
        return contact

    @classmethod
    def view_individual_contact(cls, contact: dict):
        os.system('clear')
        print(f"""Name: {contact['name']}
        Email: {contact['email']}
        Phone: {contact['phone']}
        Groups: {contact['groups']}
        Last Contact Date: {contact['follow_up']['last_contact']}""")

    @classmethod
    def view_all_contacts(cls, contacts_dict):
        print(f"\033[1m{'Name:':25}{'Email:':30}{'Phone:':18}{'Groups:'}\033[0m")
        for contact, details in contacts_dict.items():
            print(f"{details['name']:25}{details['email']:30}{details['phone']:18}{details['groups']}")
