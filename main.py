import os
import pytest
import requests
from datetime import datetime as dt
import re


class Expenses:
    def __init__(self, exp_list: list = None):
        # [Expense] acts as placehold for a list containing future Expenses
        self.expenses = exp_list if exp_list else []


class ExpensesAPI:
    def __init__(self):
        self.base_url = 'http://127.0.0.1:5000'
        self.endpoint = '/expenses'
        self.url = self.base_url + self.endpoint

    def load_expenses(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            
            return response.json()

        except ConnectionError:
            print("[ERROR] Can't connect to API")
        except ConnectionRefusedError:
            print("[ERROR] Connection refused")
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 404:
                print(f"[ERROR] API says not found (404)")
            else:    
                print(f"[ERROR] HTTP Error: {err}")
        except Exception as e:
            print(f"No...\n{e}")
            
    def add_expense(self, expense):
        try:
            response = requests.post(self.url, json=expense)
            response.raise_for_status()
            return response
        
        except ConnectionError:
            print("[ERROR] Can't connect to API")
        except ConnectionRefusedError:
            print("[ERROR] Connection refused")
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 404:
                print(f"[ERROR] API says not found (404)")
            else:    
                print(f"[ERROR] HTTP Error: {err}")
        except Exception as e:
            print(f"No...\n{e}")
    
    def edit_expense(self, expense_id, expense):
        try:
            response = requests.put(f"{self.url}/{expense_id}", json=expense)
            response.raise_for_status()
            return response

        except ConnectionError:
            print("[ERROR] Can't connect to API")
        except ConnectionRefusedError:
            print("[ERROR] Connection refused")
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 404:
                print(f"[ERROR] API says not found (404)")
            else:    
                print(f"[ERROR] HTTP Error: {err}")
        except Exception as e:
            print(f"No...\n{e}")
    
    def del_expense(self, expense_id):
        try:
            response = requests.delete(f"{self.url}/{expense_id}")
            response.raise_for_status()
            return response

        except ConnectionError:
            print("[ERROR] Can't connect to API")
        except ConnectionRefusedError:
            print("[ERROR] Connection refused")
        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 404:
                print(f"[ERROR] API says not found (404)")
            else:    
                print(f"[ERROR] HTTP Error: {err}")
        except Exception as e:
            print(f"No...\n{e}")


def create_expense():
    exp_desc = ""
    # keeps asking for a task name until user enters something
    while not exp_desc:
        exp_desc = input("[EXPENSE TITLE]: ").title()
    exp_amount = 0
    while not exp_amount:
        try:
            exp_amount = int(input("[AMOUNT]: ").lower())
        except ValueError:
            print("[ERROR] Amount must be a valid number!")
    
    todays_date = dt.now().date()
    exp_date = ""
    while not exp_date:
        exp_date = input(f"[DATE YYYY-MM-DD] ({todays_date}) Enter to accept: ")
        if not exp_date:
            exp_date = todays_date
        elif not re.match(r"\d{4}-\d{2}-\d{2}", exp_date):
            exp_date = ""
            
    return {
        "description": exp_desc,
        "amount": exp_amount,
        "date": str(exp_date)
    }


def clear_screen():
    # depending on user OS, choice is made to select the right statement to clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')

def exit_program():
    clear_screen()
    show_main_screen()
    print("Thanks for using tasker 1.1, exiting...")

def view_tasks():
    clear_screen()
    show_main_screen()
    for entry in ExpensesAPI().load_expenses()["expenses"]:
        print(f"[{entry["id"]}] {entry["description"]} {entry["amount"]} {entry["date"]}")
    print()

def add_task():
    if ExpensesAPI().add_expense(create_expense()).status_code == 201:
        input("\nExpense has been added\nENTER to continue...")
    else:
        input("[ERROR] API says no\nENTER to continue...")
    clear_screen()

def edit_task():
    view_tasks()
    task_number = -1
    # keeps asking the user for a number until 0 (exit) or a valid number have been chosen
    while task_number < 0:
        try:
            task_number = int(input("[EXPENSE NUMBER or 0 to main menu] "))
        except ValueError:
            # does not give user feedback as it's not hard to choose between numbers...
            pass
    if task_number:
        if ExpensesAPI().edit_expense(task_number, create_expense()) is not None:
            input("\n[OK] Expense updated\nENTER to continue...")
        else:
            input("\n[ERROR] Couldn't update\nENTER to continue...")
    clear_screen()

def del_task():
    view_tasks()    
    task_number = -1
    # keeps asking the user for a number until 0 (exit) or a valid number have been chosen
    while task_number < 0:
        try:
            task_number = int(input("[EXPENSE NUMBER or 0 to main menu] "))
        except ValueError:
            # does not give user feedback as it's not hard to choose between numbers...
            pass
    if task_number:
        # if del_expense returns other than None
        if ExpensesAPI().del_expense(task_number) is not None:
            ## API always returns 204 regardless of real deletion happening so...
            input("\n[OK] Deletion request received\nENTER to continue...")
        else:
            input("\n[ERROR] Couldn't delete\nENTER to continue...")
    clear_screen()


def show_main_screen(options=()):
    # make sure your window is wide enough for the ASCII art to display properly
    print('''
░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓████████▓▒░▒▓███████▓▒░ ░▒▓███████▓▒░▒▓████████▓▒░▒▓███████▓▒░          ░▒▓█▓▒░      ░▒▓████████▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓████▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░         ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓██████▓▒░  ░▒▓██████▓▒░░▒▓███████▓▒░░▒▓██████▓▒░ ░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓██████▓▒░ ░▒▓███████▓▒░          ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░         ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░         ░▒▓█▓▒░▒▓██▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░         ░▒▓█▓▒░▒▓██▓▒░▒▓████████▓▒░
    ''')
        
    if options:
        # if an empty tuple has been passed it's probably a filler so ignore it
        for option in [o for o in options if o != ()]:
            # show the option number and description to the user
            print(f"[{option[0]}] {option[1]} ")

def get_user_choice(options):
    # initializes the command variable with a negative value so program flow goes inside while loop at least once        
    choice = -1
    # keeps refreshing the screen and asking for a number until a valid choice is made
    # if an empty tuple has been passed it's probably a filler so ignore it
    while choice not in [option[0] for option in options if option != ()]:
        clear_screen()
        show_main_screen(options)
        try:
            choice = int(input("Enter a command: "))
        except ValueError: # is parsing of user command to int is not successful...
            # does not give user feedback as it's not hard to choose between 4 numbers but exception must be caught so program doesn't crash
            pass
    return choice

def main():
    is_running = True
    choices = () # variable needs to be initialized once
    service_api = ExpensesAPI() # an instance is required so we can call its methods
    # if there are no tasks, limit the command choices available to the user making add task or exit the only possible choices if there's no data
    while is_running: # run indefinitely
        data = len(service_api.load_expenses()["expenses"])
        # input(f"Found {data} items")
        if data: # the data list will evaluate to false if it's empty
            choices = (
                # create nested tuple for each possible user command - (command, description and which function to call)
                (), # first tuple is empty so that option number matches its position in the nested tuple
                (1, "View existing tasks", view_tasks),
                (2, "Add a new task", add_task),
                (3, "Edit existing task", edit_task),
                (4, "Delete existing task\n", del_task),
                (0, "Exit\n", exit_program)
            )
        else:
            choices = (
                (), # first tuple is empty so that option number matches its position in the nested tuple
                (), (2, "Add a new task", add_task), (), (), (0, "Exit\n", exit_program) # several tuples are empty as the options to view, edit and delete (as well as their messages and respective functions) don't make sense if the data list is empty (Nothing to view, edit or delete at that moment in time)
            )
        clear_screen()
        show_main_screen(choices)
        
        # choice number has already been validated in "get_user_choice" so if the user gets here, things are working
        match get_user_choice(choices):
            case 1:
                choices[1][2]() # calls view_tasks()
                input("\nENTER to continue...")
                clear_screen()
            case 2: 
                choices[2][2]() # calls add_task() (stored in the choices tuple)
            case 3:
                choices[3][2]() # calls edit_task() (stored in the choices tuple)
            case 4:
                choices[4][2]() # calls del_task() (stored in the choices tuple)
            case 0:
                choices[-1][2]()
                is_running = False # calls exit_program which is always the last tuple element

# loads only a standalone python program, won't run if called as an external library
if __name__  == ("__main__"):
    main()
