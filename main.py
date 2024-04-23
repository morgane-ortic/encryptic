import time                             # allows us to use the sleep function to pause the program for a certain amount of time
import os                               # allows us to use the clear function to clear the terminal
from cryptography.fernet import Fernet  # allows us to use the Fernet class to encrypt and decrypt data
from stringcolor import cs              # allows us to use the cs function to color the text
import json                             # allows us to use the json library to work with JSON data
from flask_bcrypt import Bcrypt         # allows us to use the Bcrypt class to hash passwords
import datetime                         # allows us to use the datetime class to get the current date and time

#======================================================================================================
#Global variables
decrypted = False                  # define that the decryption process hasn't happened yet.
bcrypt = Bcrypt()                  # initialize the Bcrypt class, which we will use to hash passwords                             
usernames = ""                     # creating empty global variables to store the usernames
passwords = ""                     # creating empty global variables to store the passwords
messages = []                      # creating an empty list to store the user's messages
encMessages = ""                   # creating an empty variable to store the encrypted messages
decMessages = ""                   # creating an empty variable to store the encrypted messages
data = []                          # creating an empty list to store the user's data               
credentials = {}                   # creating an empty dictionary to store the user's credentials
fernet = None                      # creating an empty variable to store the Fernet instance
key = Fernet.generate_key()        # generates a key using the Fernet class
FILE_PATH = './users.json'         # define the path to the JSON file where we will store the user's data

#======================================================================================================
# Functions
# Defining a "clear" function that clears the terminal from previous lines
clear = lambda: os.system('clear') # allows us to use the clear function so we can use the system command 'clear' to clear the terminal

# Function that shows the main menu choices - User Interface (Only the grapchical part of the menu)part of the main menu
def main_menu_ui(): # aligning the menu items so they look nice and printing them on the screen
    print(cs("Welcome to the encryptian program. \n" , "blue"))
    print("╔" + "═" * 14 + "╗")
    print("║ 1. Login     ║" , "\n║ 2. Register  ║" , "\n║ 3. Exit      ║")
    print("╚" + "═" * 14 + "╝\n")

# Function that lets you register a new account
def register_account():
    usernames = input(cs("Enter your name: ", "cyan"))
    passwords = input(cs("Enter a passwords: ", "cyan"))
    hashed_passwords = bcrypt.generate_passwords_hash(passwords).decode('utf-8')  # Hash the password
    clear()
    initial_message = input('Would you like to enter an initial message? (yes/no): ').lower()
    while initial_message == 'yes' or initial_message == 'no' or initial_message != 'yes' or initial_message != 'no':
            if not initial_message.strip():
                initial_message = input('Yes or no? ').lower()
                time.sleep(1)
            if initial_message == 'yes' and initial_message != 'no':
                messages = input(f"Hi {cs(usernames.title(), 'cyan')}, enter the message you want to encrypt: ")
                clear()
                encryption_function()
                print(cs("Encrypting: ", "green"), end='', flush=True) 
                print(print_letters_appart(encMessages))       # print the encrypted string
                # insert_info_in_database() MySQL database function / not in use
                time.sleep(0.5)
                print(cs("\nMessage added!" , "yellow"))
                break
            elif initial_message == 'no' and initial_message != 'yes':
                clear()
                break
            else:
                clear()
                print("Would you like to input an initial message or not?.")
        message += f"\n\nMessage created at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        messages.append(fernet.encrypt(message.encode()).decode('utf-8'))  # Encrypt and add the message to the list

    # Store username, password, messages, and key in the credentials dictionary
    credentials = {
        'usernames': usernames,
        'passwords': hashed_passwords,  # Store the hashed password
        'messages': messages,
        'key': key.decode('utf-8')  # Convert the key to a string and store it
    }

    # Load existing data from the JSON file
    if os.path.exists(FILE_PATH) and os.stat(FILE_PATH).st_size != 0:
        with open(FILE_PATH, 'r') as input_file:  # Open the JSON file in read mode
            data = json.load(input_file)
            if isinstance(data, dict):  # If data is a dictionary, convert it to a list
                data = [data]
    else:
        data = []  # If the file doesn't exist or is empty, start with an empty list

    data.append(credentials)  # Append the new credentials to the list

    # Write the data back to the JSON file
    with open(FILE_PATH, 'w') as output_file:
        json.dump(data, output_file, indent=2)

    clear()  # clear the terminal
    print("Registration successful! \n")  # let user know registration worked
    time.sleep(2)  # give a 2 seconds break before next line
    clear()  # clear the terminal
    # Loading screen redirecting to login function
    print("You can now login with your new account. \n")
    print("Redirecting to login page", end='', flush=True)  # display text letter by letter
    time.sleep(0.2)
    print(".", end='', flush=True)
    time.sleep(0.2)
    print(".", end='', flush=True)
    time.sleep(0.2)
    print(".", end='', flush=True)
    time.sleep(0.2)
    print(".", end='', flush=True)
    time.sleep(0.2)
    print(".", end='', flush=True)
    time.sleep(0.2)
    print(".", end='', flush=True)
    time.sleep(1)
    clear()
    login()

# decrypt the encrypted string with the Fernet instance of the key, that was used for encrypting the string
# encoded byte string is returned by decrypt method, so we decode it to string with decode methods
def decryption(fernet, encMessage_str):
    encMessage = bytes(encMessage_str, 'utf-8')
    decMessage = fernet.decrypt(encMessage).decode()
    print("decrypted string: ", decMessage)

def load_user_data():
    global data
    if os.path.exists(FILE_PATH) and os.stat(FILE_PATH).st_size != 0:
        with open(FILE_PATH, 'r') as input_file: # Open the JSON file in read mode
            data = json.load(input_file)
            if isinstance(data, dict):  # If data is a dictionary, convert it to a list
                data = [data]
    else:
        data = []  # If the file doesn't exist or is empty, start with an empty list

def login():
    global decrypted  # Define these variables as global
    load_user_data()  # Ensure data is loaded before login
    while not decrypted:
        name_input = input("What's your name? ")
        for user in data:
            if user['usernames'].lower() == name_input.lower() and not decrypted:  # Check if the username exists in the data (case-insensitive)
                while True:  # Keep asking for the password until the correct one is entered
                    time.sleep(2)
                    passwords_input = input(f"Hello, {usernames}. Please enter your password: ")
                    hashed_passwords = user['passwords']
                    if bcrypt.check_passwords_hash(hashed_passwords, passwords_input):  # Check if the password is correct
                        time.sleep(2)
                        fernet = Fernet(user['key'])  # Initialize Fernet with the user's key
                        decrypted = True
                        if 'messages' in user:  # Check if 'messages' key exists in the user dictionary
                            for encMessage_str in user['messages']:  # Decrypt each message individually
                                decryption(fernet, encMessage_str)  # Pass the fernet instance and the encrypted message to decryption function
                        else:
                            print("No messages found.")
                        print()  # Add a newline for clarity
                        return fernet  # Return the fernet instance from the login function
                    else:
                        time.sleep(2)
                        print("This is not the password >:(")
            break



def display_messages(): # Function to display messages
    if not fernet:
        print("You need to log in first to access your messages.")
        return

    for user in data: # Find the user in the data
        if user['usernames'].lower() == usernames.lower():
            if 'messages' in user:  # Check if 'messages' key exists in the user dictionary
                for encMessage_str in user['messages']:  # Decrypt and display each message individually
                    decMessage = fernet.decrypt(bytes(encMessage_str, 'utf-8')).decode()
                    print("Decrypted message:")
                    print(decMessage)
                    print()
            else:
                print("No messages found.")
            return

def add_message(): # Function to add a message
    if not fernet: # Check if the user is logged in
        print("You need to log in first to add a message.")
        return

    new_message = input("Enter the message you want to add: ")
    new_message += f"\n\nMessage created at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    for user in data: # Find the user in the data
        if user['usernames'].lower() == usernames.lower():
            user['messages'].append(fernet.encrypt(new_message.encode()).decode('utf-8'))
            break

    with open(FILE_PATH, 'w') as output_file: # Write the updated data back to the JSON file
        json.dump(data, output_file, indent=2)

    print("Message added successfully!")
           
def show_letters(string):
    for char in string:
        time.sleep(0.03)
        print(char, end=' ', flush=True)
    return '' 

def program():
    fernet = None
    while True:
        print(cs("Welcome to the encryption program. \n", "blue"))
        time.sleep(1)

        print(' 1. Login \n', '2. Register \n', '3. Display Messages\n', '4. Add Message\n', '5. Logout\n', '6. Exit \n')
        choice = input("Enter your choice: ").lower()
        while choice not in ['login', 'register', 'display messages', 'add message', 'logout', 'exit', '1', '2', '3', '4', '5', '6']:
            choice = input("Invalid choice. Please enter a valid choice: ").lower()

        if choice == 'login' or choice == '1':
            clear()
            if not fernet:
                fernet = login()
            else:
                print("You are already logged in.")

        elif choice == 'register' or choice == '2':
            clear()
            register_account()

        elif choice == 'display messages' or choice == '3':
            clear()
            display_messages()

        elif choice == 'add message' or choice == '4':
            clear()
            add_message()
        elif choice == 'exit' or choice == '6':
            clear()
            print(cs("Exiting program", "magenta"))
            time.sleep(2)
            exit()

# Function that encrypts the message inputed by the user
def encryption_function():
    fernet = Fernet(key)            # We tell the Fernet class to use the key we generated
    encMessages = fernet.encrypt(messages.encode()) # Encrypt the messages / to encrypt the string it must be encoded to byte string before encryption_function

# Function that decrypts an encrypted message
def decryption_function():                                    
    fernet = Fernet(key)
    decMessages = fernet.decrypt(encMessages).decode() # decrypting the encrypted string with the same Fernet instance that was used for encrypting the string

# Function that prints out string characters one by one
def print_letters_appart(string):
    for char in string:
        time.sleep(0.03)
        print(char, end=' ', flush=True)
    return '' 

#======================================================================================================
# This is where the program starts. Registration and login functions are called here.

clear()     # calling the clear function to clear the terminal at the start of the program
program()   # Call the program function to start the program


