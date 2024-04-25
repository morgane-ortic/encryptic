#Libaries used in the program:: - we put them here to shorten the code and make the code more readable

import datetime                         # allows us to work with dates and times
import json                             # allows us to work with JSON files
import time                             # allows us to work with time / different frin datetime
import os                               # allows us to interact with the operating system
from cryptography.fernet import Fernet  # allows us to encrypt and decrypt data
from flask_bcrypt import Bcrypt         # allows us to hash passwords
from stringcolor import cs              # allows us to color the text in the terminal
import weather                          # allows us to work with the weather.py file which helps us to get the weather data

#======================================================================================================
#Global variables - variables that are used in multiple functions:: - we put them here to shorten the code and make the code more readable

usernames = ""                          # variables that store the username inputed by the user
passwords = ""                          # variables that store the password inputed by the user
message = ""                            # variable that stores the message inputed by the user
messages = ""                           # variable that stores the message inputed by the user
messages_list = []                      # list that stores the messages
credentials = {}                        # dictionary that stores the credentials
key = Fernet.generate_key()             # generate a key for the encryption globaly
fernet = Fernet(key)                    # create a Fernet instance with the key globaly
encMessages = ""                        # variable that stores the encrypted messages
bcrypt = Bcrypt()                       # create an instance of the Bcrypt class                                                           
name_input = ""                         # variable that stores the name inputed by the user after logging in
data = []                               # list that stores the data from the JSON file
JSON_FILE = './users.json'              # variable that stores the path to the JSON file for easier use later in the code

#======================================================================================================
# Functions::

clear = lambda: os.system('clear')      # define a "clear" function that clears the terminal from previous lines
clear()                                 # call the clear function to clear the terminal

def main_menu_ui():         # Function that shows the main menu choices - User Interface (Graphical part of the main menu) - ONLY PRINTING
    print(cs("Welcome to the encryption program. \n" , "blue"))             # print the welcome message
    weather.main()                                                          # call the weather.main() function to get the weather data
    print("\n")                                                             # print a new line 
    print("╔" + "═" * 14 + "╗")                                             # print the top border of the main menu
    print("║ 1. Login     ║" , "\n║ 2. Register  ║" , "\n║ 3. Exit      ║") # print the choices of the main menu
    print("╚" + "═" * 14 + "╝\n")                                           # print the bottom border of the main menu

def main_menu_logic():      # Function that works as the main menu of the program (logical part of the main menu)
    main_menu_ui()          # Call and show the main menu choices
    main_menu_choice = ""   # variable that stores the choice of the user in the main menu
    while True:             # loop that runs until the user enters a valid choice from the main menu options (login, register, exit)
        main_menu_choice = input("Enter your choice: ").lower()             # ask the user to enter a choice - it gets lowercased to make it easier to compare
        clear()                                                             #
        main_menu_ui()                                                      # call the main menu UI to show the choices again after clearing the terminal
        if main_menu_choice == 'login' or main_menu_choice == '1':          # if the user enters 'login' or '1' - the program will allow the user to login
            clear()                                                         #
            logging_in()                                                    # the logging_in function will be called so the the user can input their username and password
            logged_in_menu_logic()                                          # call the logged_in_menu_logic function to show the choices after logging in
        elif main_menu_choice == 'register' or main_menu_choice == '2':     # if the user enters 'register' or '2' - the program will allow the user to register
            clear()                                                         #
            register_account()                                              # the register_account function will be called so the user can register a new account
        elif main_menu_choice == 'exit' or main_menu_choice == '3':         # if the user enters 'exit' or '3' - the program will stop running
            clear()                                                         #
            print(cs("Exiting program", "magenta") , end='', flush=True)    # print the message that the program is exiting
            print(print_letters_appart(20 * '.'))                           # print the dots separately to make the program look like it's exiting
            time.sleep(0.5)                                                 # wait for 0.5 seconds before exiting (all special effects basically)
            clear()                                                         #
            exit()                                                          # this is where the program finally stops running
        elif (not main_menu_choice.strip or main_menu_choice != 'login' or 'register' or # if the user enters something other than 'login' or 'register' or 'exit' or '1' or '2' or '3'
            'exit' or '1' or '2' or '3' ()):                                # here a sick technique is used allowing us to write the condition in multiple lines for better readability       
            print("Please enter a valid choice.")                           # print the message that the user needs to enter a valid choice
            time.sleep(1)                                                   #
            clear()                                                         #
            main_menu_ui()                                                  # call the main menu UI to show the choices again so the user can see and choose what to enter
            continue                                                        # continue the loop until the user enters a valid choice
        break                                                               # break the loop when the user enters a valid choice

def register_account():     # Function that lets you register a new account
    global messages, usernames, passwords                         # like this we are able to use the variables in the function without giving them values
    while True:                                                   # loop that runs until the user enters a valid username
        usernames = input(cs("Enter a new username: ", "cyan"))   # ask the user to enter a new username and color the text in cyan
        if not usernames.strip():                                 # if the username is blank '.strip()' removes the whitespace from the string
            print("Username cannot be blank. Please try again.")  # print the message that the username cannot be blank
            time.sleep(1)                                         #
            clear()                                               #
            continue                                              # continue the loop until the user enters a valid username
        else:                                                     # we put else just to complete the if statement, we don't need it
            break                                                 # break the loop when the user enters a valid username
    while True:                                                   # loop that runs until the user enters a valid password
        passwords = input(cs("Enter a new password: ", "cyan"))   # ask the user to enter a new password and color the text in cyan
        if not passwords.strip():                                 # if the password is blank '.strip()' removes the whitespace from the string
            print("Password cannot be blank. Please try again.")  # print the message that the password cannot be blank
            time.sleep(1)                                         
            clear()                                               
            continue                                              
        else:                                                      
            hashed_passwords = bcrypt.generate_password_hash(passwords).decode('utf-8')  # Hash the password - convert the password to a string and stores it in the variable
            clear()
            break 
    while True:
        print('Would you like to enter an initial message? (yes/no): ')
        initial_message = input().lower()                                 # ask the user if they want to enter an initial message and lower the input
        if not initial_message.strip():                                   # if the input is blank '.strip()' removes the whitespace from the string
            print('Yes or no? ')                                          #
            time.sleep(1)                                                 #
            clear()                                                       #
        if initial_message.startswith('y'):                                      # if the user enters 'yes' - the program will allow the user to enter a message
            clear()                                                       #
            messages = input(f"Hi {cs(usernames.title(), 'cyan')}, enter the message you want to encrypt: ") # ask the user to enter a message
            adding_date_to_message()                                      # add the date and time to the message
            clear()                                                       #
            encryption_function()                                         # encrypt the message
            print(cs("Encrypting: ", "green"), end='', flush=True)        # print the message that the program is encrypting the message (a visual effect)
            print(print_letters_appart(encMessages))                      # print the dots separately to make the program look like it's encrypting the message and loading
            print(cs("\nMessage added!" , "yellow"))                      #
            break                                                         # break the loop when the user enters a valid message
        elif initial_message.startswith('n'):                                     # if the user enters 'no' - the program will not allow the user to enter a message
            clear()                                                       #
            break                                                         # break the loop when the user enters 'no'
        elif initial_message != 'yes' or initial_message != 'no':         # if the user enters something other than 'yes' or 'no'
            print('Would you like to enter an initial message? (yes/no): ')
            clear() 
            

    credentials = { # With this code we store the usernames, passwords, messages and keys of the user in the credentials dictionary
    'username': usernames,         # Store the username
    'password': hashed_passwords,  # Store the hashed password
    'messages': messages,          # Store the message
    'key': key.decode('utf-8')}    # Convert the key to a string and store it
    
    load_user_data()                              # Load the user data from the JSON file before registration
    data.append(credentials)                      # adding the new credentials to the list
    with open(JSON_FILE, 'w') as output_file:     # Write the data back to the JSON file
        json.dump(data, output_file, indent=2)    # We use dump to store/trasfer the data to the JSON file

    print(cs("\nRegistration successful!" , "yellow"))                   #
    time.sleep(2)                                                        #
    clear()                                                              #
    print(cs("Redirecting to main menu", "orange"), end='', flush=True)  #
    print(print_letters_appart(20 * '.'))                                # - All of these lines are just for the visual effect of the program
    time.sleep(0.5)                                                      #
    clear()                                                              #
    print("You can now login with your new account. ")                   #
    time.sleep(3)                                                        #
    clear()                                                              #
    main_menu_logic()                                                    # calling the main menu logic function to show the choices again after registration

def logging_in():           # Function that lets you login to your account
    load_user_data()                                                     # Load the user data from the JSON file before login, allows us to work with the data
    global usernames, passwords, name_input                              # like this we are able to use the variables in the function without giving them values again, we save space
    while True:                                                          # loop that runs until the user enters a valid username
        name_input = input(cs("Enter your username: ", "cyan"))          # ask the user to enter their username and color the text in cyan
        if not name_input.strip():                                       # if the username is blank '.strip()' removes the whitespace from the string
            print("The username cannot be blank. Please try again.")     # print the message that the username cannot be blank
            time.sleep(1)                                                #
            clear()                                                      #
            continue                                                     # continue the loop until the user enters a valid username
        elif name_input in [user['username'] for user in data]:          # if the username is in the data list
            passwords_input = input(cs("Enter your password: ", "cyan")) # ask the user to enter their password and color the text in cyan
            if not passwords_input.strip():                              # if the password is blank '.strip()' removes the whitespace from the string
                print("Password cannot be blank. Please try again.")     # print the message that the password cannot be blank
                time.sleep(1)                                            
                clear()                                                  
                continue                                                 # we check if the password corresponds to the usernames password in the json file
            elif bcrypt.check_password_hash([user['password'] for user in data if user['username'] == name_input][0], passwords_input): 
                print(cs("Logging in", "yellow"), end='', flush=True)    # print the message that the program is logging in the user (if the password is correct)
                print(print_letters_appart(20 * '.'))                    
                time.sleep(0.5)
                clear()
                break
            else:
                print(cs("Incorrect password >:()", "red"))              # print the message that the password is incorrect
            logging_in()                                                 # call the logging_in function to allow the user to enter the username and password again
        else:                                                            # if the username is not in the data list
            while True:                                                  # loop that runs until the user enters a valid choice
                print(cs("Non-existent username >:()", "red"))           # print the message that the username does not exist
                print("\nWould you like to register? (yes/no) ")         # ask the user if they want to register
                question = input().lower()                               # ask the user to enter 'yes' or 'no' and lower the input
                if not question.strip():                                 # if the input is blank '.strip()' removes the whitespace from the string
                    print("Yes or no?")                                  # print the message that the user needs to enter 'yes' or 'no'
                    time.sleep(1)                                        #
                    clear()                                              #
                elif question == 'yes':                                  # if the user enters 'yes' - the program will allow the user to register
                    clear()                                              #
                    print("Redirecting to registration page", end='', flush=True) # print the message that the program is redirecting to the registration page
                    print(print_letters_appart(20 * '.'))                #
                    clear()                                              #
                    register_account()                                   # call the register_account function to allow the user to register
                    break                                                # break the loop when the user enters 'yes'
                elif question == 'no':                                   # if the user enters 'no' - the program will not allow the user to register
                    clear()                                              #
                    print("Redirecting to main menu", end='', flush=True)# print the message that the program is redirecting to the main menu
                    print(print_letters_appart(20 * '.'))                #
                    clear()                                              #
                    main_menu_logic()                                    # call the main_menu_logic function to show the choices again after logging in
                    break                                                # break the loop when the user enters 'no'
                else:                                                    # if the user enters something other than 'yes' or 'no'
                    print("Invalid input. Please enter 'yes' or 'no'.")  # print the message that the user needs to enter 'yes' or 'no'
                    time.sleep(1)                                        #
                    clear()                                              #

def logged_in_menu_ui():    # Function that shows the logged in menu choices - User Interface (Graphical part of the logged in menu) - ONLY PRINTING
    print(cs("Welcome to the encryption program. \n" , "blue"))
    print( 'Hello ' , (cs(f"{name_input.title()} \n", "cyan")))
    weather.main()                                                          # call the weather.main() function to get the weather data
    print("\n")                                                             # print a new line 
    print("╔" + "═" * 22 + "╗")
    print("║ 1. Display message   ║" , "\n║ 2. Add Message       ║" , "\n║ 3. Delete Message    ║")
    print("║ 4. Delete Account    ║" , "\n║ 5. Log out           ║" , "\n║ 6. Exit              ║")
    print("╚" + "═" * 22 + "╝\n")

def logged_in_menu_logic(): # Function that works as menu afterlogging in (logical part of the logged in menu) 
    logged_in_menu_ui()                                     # Calling and showing the menu choices after logging in (UI part)
    global messages, fernet                                   # like this we are able to use the variables in the function without giving them values
    logged_in_choice = input("Enter your choice: ").lower() # ask the user to enter a choice - it gets lowercased to make it easier to compare
    while (logged_in_choice != 'display messages' or 'add message' or 'delete message' or 
           'log out' or 'exit' or '1' or '2' or '3' or '4' or '5'): # loop that runs until the user enters a valid choice from the logged in menu options
        if logged_in_choice == 'display messages' or logged_in_choice == '1': # if the user enters 'display messages' or '1' - the program will display the messages
            clear()                                         #
            load_user_data()                                # allows us to work with the data from the JSON file
            read_messages_from_json()                       # reads the messages from the JSON file
            print(cs("Displaying messages", "magenta"))     #      
            messages = read_messages_from_json()            # read the messages from the JSON file
            for message in messages:                        # loop that runs through the messages for every message in the messages list in the currently logged in user
                print(message)                              # print the messages
            input("\nPress Enter to continue...")           # ask the user to press Enter to continue, allows for better user experience
            clear()                                         #
            logged_in_menu_logic()                          # call the logged_in_menu_logic function to show the choices after going out of the list of messages
            break                                           
        elif logged_in_choice == 'add message: ' or logged_in_choice == '2': # if the user enters 'add message' or '2' - the program will allow the user to add a another message
            clear()                                         # messages added this way will be tacked below the previous message
            messages = input(cs("Enter a new message: ", "cyan")) # ask the user to enter a new message and color the text in cyan            
            print(cs("Encrypting: ", "green"), end='', flush=True)# print the message that the program is encrypting the message (a visual effect) 
            adding_date_to_message()                        # add the date and time to the message
            write_to_json()                                 # write the message to the JSON file which includes the date and time as well
            add_message_in_json(name_input, messages)       # add the message to the JSON file
            print(print_letters_appart(encMessages))        # print the dots separately to make the program look like it's encrypting the message and loading
            time.sleep(2)                                   #
            clear()                                         #
            logged_in_menu_logic()                          # call the logged_in_menu_logic function to show the choices after adding the message
            break                                            
        elif logged_in_choice == 'delete message' or logged_in_choice == '3': # if the user enters 'delete message' or '3' - the program will allow the user to delete the message
            clear()                                         #
            delete_messages()                               # call the delete_messages function to delete the message
        elif logged_in_choice == 'delete account' or logged_in_choice == '4': # if the user enters 'delete account' or '4' - the program will log out the user
            clear()                                                              #
            delete_account()                                                     # call the delete_account function to delete the account
        elif logged_in_choice == 'log out' or logged_in_choice == '5':           # if the user enters 'log out' or '4' - the program will log out the user
            clear()                                                              #
            print(cs("Logging out", "magenta"), end='', flush=True)              #
            print(print_letters_appart(20 * '.'))                                #
            time.sleep(0.5)                                                      # - A lot of visual effects to make the program look more interesting
            clear()                                                              #
            print(cs("Redirecting to main menu", "orange"), end='', flush=True)  #
            print(print_letters_appart('..........\n\n'))                        #
            clear()                                                              # 
            main_menu_logic()                                                    # call the main_menu_logic function to show the choices after logging out
        elif logged_in_choice == 'exit' or logged_in_choice == '5':              # if the user enters 'exit' or '5' - the program will stop running
            clear()                                                              #
            print(cs("Exiting program", "magenta") , end='', flush=True)         #
            print(print_letters_appart(20 * '.'))                                #
            time.sleep(1.5)                                                      #   
            clear()                                                              #
            exit()                                                               # this is where the program finally stops running - os.exit() is used to stop the program

def load_user_data():       # Function that loads the user data from the JSON file
    global data                                 
    if os.path.exists(JSON_FILE) and os.stat(JSON_FILE).st_size != 0: # Check if the JSON file exists and is not empty
        with open(JSON_FILE) as json_file:                            # Open the JSON file in read mode
            data = json.load(json_file)                               # Load the data from the JSON file
            if isinstance(data, dict):                                # If 'data' is a dictionary, convert it to a list
                data = [data]                                         # This is done to make the data easier to work with
    else:                                                             #
        data = []                                                     # If the file doesn't exist or is empty, start with an empty list

def read_from_json():       # Function that reads the data from the JSON file
    with open(JSON_FILE, 'r') as json_file: # Open the JSON file in read mode
        data = json.load(json_file)         # Load the data from the JSON file
    return data                             # Return the data

def write_to_json():        # Function that writes the data to the JSON file
    global JSON_FILE, data                    # we have to use JSON_FILE and data as global variables - otherwise it doesnt work
    with open(JSON_FILE, 'w') as json_file:   # Open the JSON file in write mode
        json.dump(data, json_file, indent=2)  # Write the data to the JSON file

def read_messages_from_json(): # Function that reads the messages from the JSON file / specifically the messages of the logged in user
    global JSON_FILE, data, name_input, key  # 
    with open(JSON_FILE, 'r') as json_file:  # Open the JSON file in read mode
        data = json.load(json_file)          # Load the data from the JSON file
        messages = [user['messages'] for user in data if user['username'] == name_input]  # Extracting only the "messages" field from the loggedin user's dictionary 
    return messages                          # Return the messages

def add_message_in_json(name_input, messages): # Function that adds a message to the JSON file
    global data                              # we have to use data as a global variable - otherwise it doesnt work
    for user in data:                        # Loop through the data list
        if user['username'] == name_input:   # If the username is the same as the logged in user's username
            if 'messages' in user:           # If the user has messages
                user['messages'] += f"\n{messages}" # Add the message to the user's messages
            else:                            # If the user doesn't have messages
                None                         # Do nothing
    write_to_json()                          # Write the data (aka the new message) to the JSON file

# NOT WORKING - I DONT KNOW IF IT WORKS AT ALL
"""def delete_message_from_json(name_input, messages): # Function that deletes a message from the JSON file
    global data                                     #
    for user in data:                               # Loop through the data list
        if user['username'] == name_input:          # If the username is the same as the logged in user's username
            if 'messages' in user:                  # If the user has messages
                user['messages'] = ""               # Delete the message
            else:                                   # If the user doesn't have messages
                None                                # Do nothing
    write_to_json() """                                # Write the data (aka the deleted message) to the JSON file

def delete_messages():
    global name_input, messages_list
    print("Select the message you want to delete:")
    for i, message in enumerate(messages_list):
        print(f"{i+1}. {message}")
    choice = input("Enter the number of the message you want to delete (or 'q' to cancel): ")
    if choice == 'q':
        return
    try:
        index = int(choice) - 1
        if index < 0 or index >= len(messages_list):
            print("Invalid choice. Please try again.")
            delete_messages()
        else:
            del messages_list[index]
            print("Message deleted successfully.")
            write_to_json()  # Update the JSON file with the modified messages list
    except ValueError:
        print("Invalid choice. Please try again.")
        delete_messages()    


def encryption_function(): # Function that encrypts the message inputed by the user
    global messages, encMessages, fernet
    encMessages = fernet.encrypt(messages.encode()) # Encrypt the messages / to encrypt the string it must be encoded to byte string before encryption_function

def decryption_function(): # Function that decrypts an encrypted message  
    global fernet, message, decMessages
    decMessages = fernet.decrypt(message.encode()).decode() # decrypting the encrypted string with the same Fernet instance that was used for encrypting the string

def print_letters_appart(string): # Function that prints out string characters one by one
    for char in string:                   # loop that runs through the characters in the string
        time.sleep(0.03)                  # wait for 0.03 seconds before printing the next character
        print(char, end=' ', flush=True)  # print the character and flush the output buffer
    return ''                             # return an empty string

def adding_date_to_message(): # Function that adds the date and time to the message
    global messages
    messages += f" - Message created at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" # Add the date and time to the message
    messages_list.append(fernet.encrypt(messages.encode()).decode('utf-8'))                       # Encrypt and add the message to the list       

def delete_account():
    global name_input, data, JSON_FILE
    while True:
        confirmation = input("Are you sure you want to delete your account? (yes/no): ").lower()
        if confirmation.startswith('y'):
            data = [user for user in data if user['username'] != name_input]
            write_to_json()
            print(cs("Account deleted successfully!", "yellow"))
            time.sleep(2)
            clear()
            print(cs("Redirecting to main menu", "orange"), end='', flush=True)
            print(print_letters_appart(20 * '.'))
            time.sleep(0.5)
            clear()
            main_menu_logic()
            break
        elif confirmation.startswith('n'):
            clear()
            logged_in_menu_logic()
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
            time.sleep(1)
            clear()

main_menu_logic() # This is where the program starts.
