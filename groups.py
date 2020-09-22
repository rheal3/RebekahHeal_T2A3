import inquirer

class Groups:
    @classmethod
    def add_group(cls, groups_list):
        def group_validation(answers, current):
            if current in groups_list:
                inquirer.ValidationError('', reason="Group name in use.")
            return True

        def day_validation(answers, current):
            if not current.isnumeric():
                inquirer.ValidationError('', reason="Invalid data type. Numbers only.")
            return True

        group = inquirer.prompt([inquirer.Text('group', message="Group Name", validate=group_validation), inquirer.Text('days', message="Number Of Days Between Contact", validate=day_validation)])
        groups_list[group['group']] = group['days']
        print(groups_list)

groups_list = {} #user_data[username]['groups_list']  <- select using keys
Groups.add_group(groups_list)
Groups.add_group(groups_list)
Groups.add_group(groups_list)

print(groups_list)
