
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
