
def view_mine():
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




