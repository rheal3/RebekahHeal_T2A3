from file import File # remove later, just for testing :)
from googleapiclient.discovery import build # remove after testing.
import inquirer
from manage_contacts import ManageContacts
from datetime import datetime, timedelta, date
from termcolor import cprint
from send_email import SendEmail

class FollowUp:
    @staticmethod
    def follow_up_menu():
        options = inquirer.prompt([inquirer.List('choice', message="Choose Option", choices=['View Follow Up', 'Follow Up By Email'])])
        if options['choice'] == 'View Follow Up':
            FollowUp.view_follow_up(contacts_dict)
        elif options['choice'] == 'Follow Up By Email':
            pass


    @classmethod
    def set_dates(cls, selected_contact, groups_dict): #Call within follow up function to get next date.. after follow up :)
        if len(selected_contact['groups']) > 0:
            nearest_contact = min([int(groups_dict[group]) for group in selected_contact['groups']])
            selected_contact['follow_up']['last_contact'] = datetime.today().strftime("%Y-%m-%d")
            selected_contact['follow_up']['next_contact'] = (datetime.today() + timedelta(days=nearest_contact)).strftime("%Y-%m-%d")
            print(selected_contact)
        else:
            print("Add contact to group to set next follow up date.")

    @classmethod
    def view_follow_up(cls, contacts_dict):
        def days_between(date):
            today = datetime.today()
            date = datetime.strptime(date, "%Y-%m-%d")
            return abs((date - today).days)

        all_contacts = {contact:details['follow_up']['next_contact'] for contact, details in contacts_dict.items()}
        contact_dates = [date for contact, date in all_contacts.items()]
        done = []

        print(f"{'Name:':20}{'Next Contact Date:'}")
        while len(all_contacts) != len(done):
            min_date = min(contact_dates)
            for contact, date in all_contacts.items():
                if date == min_date and contact not in done:
                    if days_between(date) <= 1:
                        cprint(f"{contact:20}{date}", 'red')
                    elif days_between(date) <= 3:
                        cprint(f"{contact:20}{date}", 'yellow')
                    else:
                        print(f"{contact:20}{date}")
                    done.append(contact)
                    contact_dates.remove(min_date)

    @classmethod
    def get_email_contents(cls):
        print("Enter/Paste email content. Use Ctrl-D to save.")
        contents = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            contents.append(line)
        return "\n".join(contents)

    @classmethod
    def send_email(cls, current_user):
        to = ManageContacts.select_contact(contacts_dict)['email']
        subject = inquirer.text(message="Enter email subject")
        message_text = FollowUp.get_email_contents()
        # clear screen
        print(f"\n{message_text}\n")
        send = inquirer.confirm("Are you sure you want to send?", default=False)
        if send:
            SendEmail.send_message(service, SendEmail.create_message(to, subject, message_text))
        else:
            print("Message deleted.")





# last_follow_up = user_data[username][contact<-select_contact][last_contact]

file_path = 'client.json'
user_data = File.load_data(file_path)
current_user = 'test'

contacts_dict = user_data[current_user]['contacts']

groups_list = user_data[current_user]['groups_dict'].keys() # import from groups function
groups_dict = user_data[current_user]['groups_dict']
service = build('gmail', 'v1', credentials=SendEmail.get_credentials(current_user))


# FollowUp.set_dates(ManageContacts.select_contact(contacts_dict), groups_dict)
# File.save_to_file(file_path,user_data)
# FollowUp.view_follow_up(contacts_dict)
# email_contents = FollowUp.get_email_contents()
# print(email_contents)
FollowUp.send_email(current_user)
