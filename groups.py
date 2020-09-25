import inquirer
from file import File
import os

class Groups:
    groups_options = ['Add Group', 'Edit Group', 'View All Groups', 'Add Users To Group', 'Go Back'] # return to main option
    @staticmethod
    def groups_menu(user_data, groups_dict, file_path, contacts_dict, current_user):
        os.system('clear')
        if len(groups_dict) > 0:
            options = inquirer.prompt([inquirer.List('choice', message="Select Option", choices=Groups.groups_options)])
        else:
            options = inquirer.prompt([inquirer.List('choice', message="Select Option", choices=['Add Group', 'Go Back'])])

        os.system('clear')
        if options['choice'] == 'Add Group':
            Groups.add_group(groups_dict)
            File.save_to_file(file_path, user_data)
        elif options['choice'] == 'Edit Group':
            Groups.edit_groups(Groups.select_group(groups_dict), groups_dict, contacts_dict)
            File.save_to_file(file_path, user_data)
        elif options['choice'] == 'View All Groups':
            Groups.view_all_groups(groups_dict, contacts_dict)
        elif options['choice'] == 'Add Users To Group':
            Groups.add_contacts_to_group(contacts_dict, Groups.select_group(groups_dict), groups_dict)
            File.save_to_file(file_path, user_data)
        elif options['choice'] == 'Go Back':
            from user import User
            User.main_menu(user_data, contacts_dict, groups_dict, file_path, current_user)

        Groups.groups_menu(user_data, groups_dict, file_path, contacts_dict, current_user)

    @classmethod
    def day_validation(cls,answers, current):
        if not current.isnumeric():
            inquirer.ValidationError('', reason="Invalid data type. Numbers only.")
        return True

    @classmethod
    def add_group(cls, groups_dict):
        def group_validation(answers, current):
            if current in groups_dict.keys():
                inquirer.ValidationError('', reason="Group name in use.")
            current = current.lower() #NOT COMING OUT AS LOWER.. HOW TO CHANGE??
            return True

        group = inquirer.prompt([inquirer.Text('group', message="Group Name", validate=group_validation), inquirer.Text('days', message="Number Of Days Between Contact", validate=Groups.day_validation)])
        groups_dict[group['group'].lower()] = group['days']

    # same as select_contact <- create one function for both? where?
    @classmethod
    def select_group(cls, groups_dict: dict) -> dict:
        choice = inquirer.prompt([inquirer.List('selected', message='Select Group', choices=groups_dict.keys())])
        return choice['selected']

    @classmethod
    def edit_groups(cls, selected_group, groups_dict, contacts_dict):
        def group_validation(answers, current):
            if current in groups_dict.keys():
                inquirer.ValidationError('', reason="Group name in use.")
            return True

        os.system('clear')
        edit = inquirer.prompt([inquirer.List('field', message='Choose field to edit', choices=['Group Name', 'Days Between Contact', 'Remove Group'])])

        os.system('clear')
        if edit['field'] == 'Group Name':
            edit = inquirer.prompt([inquirer.Text('name', message='Enter new group name', validate=group_validation)])
            edit['name'] = edit['name'].lower()
            groups_dict[edit['name']] = groups_dict.pop(selected_group)
            for contact in contacts_dict:
                if selected_group in contacts_dict[contact]['groups']:
                    contacts_dict[contact]['groups'].remove(selected_group)
                    contacts_dict[contact]['groups'].append(edit['name'])
        elif edit['field'] == 'Days Between Contact':
            edit = inquirer.prompt([inquirer.Text('days', message='Enter new days between contact', validate=Groups.day_validation)])
            groups_dict[selected_group] = edit['days']
        elif edit['field'] == 'Remove Group':
            check = inquirer.confirm("Are you sure you want to delete?", default=False)
            if check:
                del groups_dict[selected_group]
                print("Deleted.")


    @classmethod
    def view_all_groups(cls, groups_dict, contacts_dict):
        print(f"\033[1m{'Group Name:':20}{'Days Between Contact:':30}{'Contacts In Group:'}\033[0m")
        for group, days in groups_dict.items():
            contact_in_group = [contact for contact, info in contacts_dict.items() if group in info['groups']]
            if len(days) == 1:
                days = '0' + days
            print(f"{group:20}{days} {'days':27}{str(contact_in_group)}")
        input("Press Enter to Continue")

    @classmethod
    def add_contacts_to_group(cls, contacts_dict, selected_group, groups_dict):
        os.system('clear')
        message = f"Add contacts to {selected_group}"
        selected = inquirer.prompt([inquirer.Checkbox('contacts', message=message, choices=contacts_dict.keys())])
        for contact in selected['contacts']:
            if selected_group not in contacts_dict[contact]['groups']:
                contacts_dict[contact]['groups'].append(selected_group)
                from follow_up import FollowUp
                FollowUp.set_dates(contacts_dict[contact], groups_dict)
