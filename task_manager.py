# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


#====Defining functions====
        
# Function that adds a new user to the user.txt file:
def reg_user(username_password):
        
    while True:
        new_username = input("New Username: ")
        if new_username in username_password.keys():
            print("""The username already exists in the system.
Please choose a different username""")
            continue
        break
        
    # - Request input of a new password
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password
            
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))
            
    # - Otherwise you present a relevant message.
    else:
        print("Passwords do no match")


# Function that adds a new task to the user.txt file:
def add_task(username_password, task_list):

    while True:
        '''Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
             - A username of the person whom the task is assigned to,
             - A title of a task,
             - A description of the task and 
             - the due date of the task.'''
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            continue
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("Invalid datetime format. Please use the format specified")
        break


    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")


# Function that allows the user to select and update a task:
def update_task(display_list):
    
    record = len(display_list)
    number_of_tasks = range(record)
    # Ask user to select a task.
    task_num = input("""
Please enter the corresponding number of the task that you would like
to update, or enter -1 to return to the main menu: """)
    if task_num == "-1":
        print("\nYou have chosen to return to the main menu!")
    
    elif not task_num.isdigit():
        print("\nYou have not selected a valid task!")
    
    elif int(task_num) - 1 in number_of_tasks:
        index_num = int(task_num) - 1
        print(display_list[index_num])

        # Finding the index of the user's task.
        pos_list = []
        for task in task_list:
            if task['username'] == curr_user:
                pos_list.append(task_list.index(task))
            
        index_to_use = pos_list[index_num]

        # Request the user to choose a new option.
        option = input("""\nPlease select one of the following options below:
m - Mark the task as complete
e - Edit the task - only available for tasks yet to be completed
-1 - Return to the main menu
: """)
        
        # Mark the task as complete.

        if option.lower() == "m":
            
            # Change the value in the list and update the file.
            task_list[index_to_use]["completed"] = True

            with open("tasks.txt", "w") as task_file:
                task_list_to_write = []
                for t in task_list:
                    str_attrs = [
                        t['username'],
                        t['title'],
                        t['description'],
                        t['due_date'].strftime(DATETIME_STRING_FORMAT),
                        t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                        "Yes" if t['completed'] else "No"
                    ]
                    task_list_to_write.append(";".join(str_attrs))
                task_file.write("\n".join(task_list_to_write))
                print("\nYou have marked this task as completed!\n")
        
        # Edit the task.
        elif option.lower() == "e":
            
            if task_list[index_to_use]["completed"] == True:
                print("""\nThe task has been marked as completed, and can no longer be
changed.""")
            else:
                edit_option = input("""\nEditting menu:
u - change the username to whom the task is assigned
d - change the due date of the task
:
""")
                if edit_option.lower() == "u":
                    
                    while True:
                        assign_user = input("\nWho would you like to assign this task to: ")
                        if assign_user.lower() not in username_password.keys():
                            print("\nUsername does not exist!")
                        elif assign_user.lower() == curr_user:
                            print("\nThis task is already assigned to you!")
                        else:
                            task_list[index_to_use]['username'] = assign_user.lower()

                            with open("tasks.txt", "w") as task_file:
                                task_list_to_write = []
                                for t in task_list:
                                    str_attrs = [
                                        t['username'],
                                        t['title'],
                                        t['description'],
                                        t['due_date'].strftime(DATETIME_STRING_FORMAT),
                                        t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                                        "Yes" if t['completed'] else "No"
                                    ]
                                    task_list_to_write.append(";".join(str_attrs))
                                task_file.write("\n".join(task_list_to_write))
                            print(f"This task has been assigned to {assign_user.lower()}!")    
                            break
                
                elif edit_option.lower() == "d":
                    
                    while True:
                        try:
                            assign_date = input("Please enter a new due date (YYYY-MM-DD): ")
                            assign_date_time = datetime.strptime(assign_date, DATETIME_STRING_FORMAT)
                            break

                        except ValueError:
                            print("Invalid datetime format. Please use the format specified")
                        break
                    task_list[index_to_use]['due_date'] = assign_date_time
            
                    with open("tasks.txt", "w") as task_file:
                        task_list_to_write = []
                        for t in task_list:
                            str_attrs = [
                                t['username'],
                                t['title'],
                                t['description'],
                                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                                "Yes" if t['completed'] else "No"
                            ]
                            task_list_to_write.append(";".join(str_attrs))
                        task_file.write("\n".join(task_list_to_write))     
                        print(f"The due date for this task is now {assign_date_time}!")       
        
        # Return to the main menu:                        
        elif option == "-1":
            print("\nYou have chosen to return to the main menu!")
        else:
            print("\nYou have not selected a valid option!")
    else:
        print("\nYou have not selected a valid task!")
        

# Function that displays all registered tasks:
def view_all(task_list):
      
    '''Reads the task from task.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling) 
    '''

    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        if t["completed"] == True:
            disp_str += "Task Completed?  Yes\n"
        else:
            disp_str += "Task Completed?  No\n"          
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)


# Function that displays the tasks assignes to the current user:
def view_mine(task_list):
    '''Reads the task from task.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling)
    '''
    str_list = []
    num = 1
    for t in (task_list):
        if t['username'] == curr_user:
            disp_str = f"\nTask: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            if t["completed"] == True:
                disp_str += f"Task Completed?  Yes\n"
            else:
                disp_str += f"Task Completed?  No\n"            
            disp_str += f"Task Description: \n {t['description']}\n"
            print(str(num), disp_str)
            str_list.append(disp_str)
            num += 1
    if len(str_list) > 0:
        update_task(str_list)
    else:
        print("\nYou have not been assigned a task yet.")


# Function that generates text reports:
def generate_reports(task_list, username_password):
    
    # Report #1 Task Overview

    # Getting the number of tasks registered.
    number_of_tasks = len(task_list)
    
    # Getting the number of completed and uncompleted tasks.
    completed_tasks = []
    uncompleted_tasks = []
    for task in task_list:
        if task['completed'] == True:
            completed_tasks.append(task)
        elif task['completed'] == False:
            uncompleted_tasks.append(task)
        
    number_of_completed_tasks = len(completed_tasks)
    number_of_uncompleted_tasks = len(uncompleted_tasks)

    # Getting the number of overdue tasks.
    overdue_tasks = []

    # Getting the string and integer value of today's date.
    current_date = datetime.now()
    for task in task_list:
        if task['due_date'] < current_date and task['completed'] is False:
            overdue_tasks.append(task)

    number_of_overdue_tasks = len(overdue_tasks)    

    # Getting the percentage of incomplete tasks.
    percentage_of_uncompleted_tasks = (number_of_uncompleted_tasks/number_of_tasks) * 100

    # Getting the percentage of overdue, incomplete tasks.
    percentage_of_overdue_tasks = (number_of_overdue_tasks/number_of_tasks) * 100

    # Writing the data into a text file.
    with open("task_overview.txt", "w") as task_file:
        task_file.write(f"""\nTasks registered: {number_of_tasks}
Completed tasks: {number_of_completed_tasks}
Incomplete tasks: {number_of_uncompleted_tasks}\nOverdue tasks: {number_of_overdue_tasks}
Incomplete tasks percentage: {percentage_of_uncompleted_tasks}%
Overdue, incomplete tasks percentage: {percentage_of_overdue_tasks}%
""")
    
    # Report #2 User Overview

    # Getting the number of users.
    number_of_users = len(username_password)

    # Getting the number of tasks registered.
    number_of_tasks = len(task_list)

    # Statistics for each user.
    usernames = []

    for user in username_password:
        usernames.append(user)
    
    user_tasks = {}
    for user in usernames:
        user_tasks[user] = []
        for task in task_list:
            if task['username'] == user:
                user_tasks[user].append(task) 
    
    # This is where all the data to be written is stored.
    all_users_tasks = f"""Number of users: {number_of_users}
Tasks registered: {number_of_tasks}\n"""

    # Getting all the information from the dictionary.
    for user, num in user_tasks.items():
        all_users_tasks += f"\nUser {user} tasks assigned: {len(num)}"
        user_task_percentage = (len(num)/number_of_tasks) * 100
        all_users_tasks += f"""\n{user_task_percentage}% of total tasks assigned to this user"""
        comp_tasks = []
        uncomp_tasks = []
        for d in num:
            if d['completed'] == True:
                comp_tasks.append(d)
            elif d['completed'] == False:
                uncomp_tasks.append(d)
        completed_percentage = (len(comp_tasks)/len(num)) * 100
        all_users_tasks += f"""\n{completed_percentage}% of this user's tasks are completed"""
        uncompleted_percentage = (len(uncomp_tasks)/len(num)) * 100
        all_users_tasks += f"""\n{uncompleted_percentage}% of this user's tasks are not completed"""
        current_date = datetime.now()
        over_tasks = []
        for d in num:
            if d['due_date'] < current_date and d['completed'] is False:
                over_tasks.append(d)
        overdue_uncomp_percentage = (len(over_tasks)/len(num)) * 100
        all_users_tasks += f"""\n{overdue_uncomp_percentage}% of this user's tasks are incompleted and are overdue\n"""

    # Writing the user data into a text file.
    with open("user_overview.txt", "w") as user_file:
        user_file.write(all_users_tasks)
  
    print("\nReports have been generated to your directory!")


# This function displays statistics from text file logs:
def display_statistics():    

    num_users = len(username_password.keys())
    num_tasks = len(task_list)
    print("\n========== STATISTICS =============")

    # Reading from the user.txt file.
    with open('user.txt', 'r') as us_file:
        print("\n-----------------------------------")
        print(f"Number of users: \t {num_users}")
        display_us = "\nList of usernames and passwords:\n"
        for x in us_file:
            display_us += x
        print(display_us)
        print("-----------------------------------\n")
    
    # Reading from the task.txt file.
    with open('tasks.txt', 'r') as ta_file:
        print("\n-----------------------------------")
        print(f"Number of tasks: \t {num_tasks}")
        for count, x in enumerate(ta_file, 1):
            line = x.split(';')
            print(f"""\nTask {count}:
Assigned to: {line[0]}
Task title: {line[1]}
Task description: {line[2]}
Task due date: {line[3]}
Task assigned date: {line[4]}
Task completed? {line[5]}
""")


#====Main Body Of Code=====
while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Register a user
a - Add a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user(username_password)

    elif menu == 'a':
        add_task(username_password, task_list)

    elif menu == 'va':
        view_all(task_list)

    elif menu == 'vm':
        view_mine(task_list)

    elif menu == 'gr':
        generate_reports(task_list, username_password)
                
    elif menu == 'ds' and curr_user == 'admin': 
        display_statistics()
 
    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")

