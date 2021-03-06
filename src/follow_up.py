# from file import File # remove later, just for testing :)
# from googleapiclient.discovery import build # remove after testing.
import inquirer
from manage_contacts import ManageContacts
from datetime import datetime, timedelta
from termcolor import cprint
from email_setup import EmailSetup
import os


class FollowUp:
    @staticmethod
    def follow_up_menu(contacts_dict, current_user, user_data, groups_dict,
                       file_path):
        os.system('clear')
        options = inquirer.prompt([inquirer.List('choice',
                                  message="Choose Option",
                                  choices=['View Follow Up',
                                           'Follow Up By Email',
                                           'Go Back'])])

        os.system('clear')
        if options['choice'] == 'View Follow Up':
            FollowUp.view_follow_up(contacts_dict)
            input("Press Enter to continue")
        elif options['choice'] == 'Follow Up By Email':
            try:
                FollowUp.send_email(current_user, contacts_dict, groups_dict)
            except FileNotFoundError:
                input("Unable to send message. Press Enter to continue.")
            except:
                input("\nUnable to authenticate. Press Enter to continue.")

        elif options['choice'] == 'Go Back':
            from user import User
            User.main_menu(user_data, contacts_dict, groups_dict,
                           file_path, current_user)
        FollowUp.follow_up_menu(contacts_dict, current_user, user_data,
                                groups_dict, file_path)

    @classmethod
    def set_dates(cls, selected_contact: dict, groups_dict):
        if len(selected_contact['groups']) > 0:
            nearest_contact = min([int(groups_dict[group]) for group in
                                  selected_contact['groups']])
            contact = selected_contact['follow_up']
            contact['last_contact'] = (datetime.today().strftime("%Y-%m-%d"))
            contact['next_contact'] = (datetime.today() + timedelta
                                       (days=nearest_contact)).strftime(
                                       "%Y-%m-%d")
        else:
            print("Add contact to group to set next follow up date.")

    @classmethod
    def view_follow_up(cls, contacts_dict):
        os.system('clear')

        def days_between(date):
            today = datetime.today()
            date = datetime.strptime(date, "%Y-%m-%d")
            return (date - today).days

        all_contacts = {contact: details['follow_up']['next_contact']
                        for contact, details in contacts_dict.items()}
        contact_dates = [date for contact, date in all_contacts.items()
                         if date != '']
        done = [date for contact, date in all_contacts.items() if date == '']
        if len(contact_dates) > 0:
            print(f"\033[1m{'Name:':25}{'Next Contact Date:'}\033[0m")
            while len(all_contacts) != len(done):
                min_date = min(contact_dates)
                for contact, date in all_contacts.items():
                    if date == min_date and contact not in done:
                        if days_between(date) <= 1:
                            cprint(f"{contact:25}{date}", 'red')
                        elif days_between(date) <= 3:
                            cprint(f"{contact:25}{date}", 'yellow')
                        else:
                            cprint(f"{contact:25}{date}", 'green')
                        contact_dates.remove(min_date)
                        done.append(contact)
            for contact, date in all_contacts.items():
                if date == '' and contact not in done:
                    print(f"{contact:25}-")
                    done.append(contact)
        else:
            print("Add contacts to groups to view follow up dates.")

    @classmethod
    def get_email_contents(cls):
        print("Enter/Paste email content. On new line use Ctrl-D to save.")
        contents = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            contents.append(line)
        return "\n".join(contents)

    @classmethod
    def send_email(cls, current_user, contacts_dict, groups_dict):
        to = ManageContacts.select_contact(contacts_dict)
        subject = inquirer.text(message="Enter email subject")
        message_text = FollowUp.get_email_contents()

        os.system('clear')
        print(f"\nSubject: {subject}\n\n{message_text}\n")
        message = "Are you sure you want to send?"
        send = inquirer.confirm(message, default=False)
        if send:
            EmailSetup.send_message(EmailSetup.create_message(to['email'],
                                    subject, message_text), current_user)
            FollowUp.set_dates(to, groups_dict)
        else:
            print("Message deleted.")
