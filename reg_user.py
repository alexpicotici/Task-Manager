def reg_user():
        
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
