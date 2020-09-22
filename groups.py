import inquirer
from file import File

class Groups:
    @staticmethod
    def groups_menu(user_data, groups_dict, file_path):
        pass

    @classmethod
    def group_validation(cls, answers, current):
        if current in groups_dict.keys():
            inquirer.ValidationError('', reason="Group name in use.")
        return True

    @classmethod
    def day_validation(cls,answers, current):
        if not current.isnumeric():
            inquirer.ValidationError('', reason="Invalid data type. Numbers only.")
        return True

    @classmethod
    def add_group(cls, groups_dict):
        group = inquirer.prompt([inquirer.Text('group', message="Group Name", validate=Groups.group_validation), inquirer.Text('days', message="Number Of Days Between Contact", validate=Groups.day_validation)])
        groups_dict[group['group']] = group['days']

    # same as select_contact <- create one function for both? where?
    @classmethod
    def select_group(cls, groups_dict: dict) -> dict:
        choice = inquirer.prompt([inquirer.List('selected', message='Select Group', choices=groups_dict.keys())])
        return choice['selected']

    @classmethod
    def edit_groups(cls, selected_group, groups_dict):
        edit = inquirer.prompt([inquirer.List('field', message='Choose field to edit', choices=['Group Name', 'Days Between Contact'])])

        if edit['field'] == 'Group Name':
            edit = inquirer.prompt([inquirer.Text('name', message='Enter new group name', validate=Groups.group_validation)])
            groups_dict[edit['name']] = groups_dict.pop(selected_group)
        elif edit['field'] == 'Days Between Contact':
            edit = inquirer.prompt([inquirer.Text('days', message='Enter new days between contact', validate=Groups.day_validation)])
            groups_dict[selected_group] = edit['days']

    @classmethod
    def view_all_groups(cls, groups_dict):
        print(f"{'Group Name:':20}{'Days Between Contact:'}")
        for group, days in groups_dict.items():
            print(f"{group:20}{days} days")

    @classmethod
    def add_user_to_group(cls, contacts_dict, selected_group):
        # select group function -> checkbox to select users to add to group -> iterate through chose users & append group to groups
        message = f"Add contacts to {selected_group}"
        selected = inquirer.prompt([inquirer.Checkbox('contacts', message=message, choices=contacts_dict.keys())])
        for contact in selected['contacts']:
            print(selected_group)
            if selected_group not in contacts_dict[contact]['groups']:
                contacts_dict[contact]['groups'].append(selected_group)
                print(contacts_dict[contact])


user_data = File.load_data('client.json')
username = 'test'
groups_dict = user_data[username]['groups_dict']  #<- select using keys
contacts_dict = user_data[username]['contacts']

Groups.add_user_to_group(contacts_dict, Groups.select_group(groups_dict))

File.save_to_file('client.json', user_data)
