import time # import the time library that we will use lter in the code
import os # import the os library
from cryptography.fernet import Fernet # import fernet from the cryptography library, used for encryption and decryption
from stringcolor import cs # import cs from the stringcolor library
import json
from flask_bcrypt import Bcrypt
import datetime

clear = lambda: os.system('clear') # define a "clear" function that clears the terminal from previous lines
clear() # call the clear function to clear the terminal

#Global variables
decrypted = False # define that the decryption process hasn't happened yet.
# create empty variables that we will use to store the values we define later
# It's not necessary in this code, but it's good practice and helps with readability
bcrypt = Bcrypt()
username = ""
password = ""
message = ""
credentials = {}

FILE_PATH = './users.json'

# Functions
# Register a new user, password and message and encrypts the message:
def register():
    global username, password, fernet  # Define these variables as global
    # Ask the user for username, password, and message
    username = input(cs("Enter your name: ", "cyan"))
    password = input(cs("Enter a password: ", "cyan"))
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')  # Hash the password

    messages = []  # Initialize an empty list to store messages

    # Generate a key for encryption and decryption using Fernet
    key = Fernet.generate_key()
    fernet = Fernet(key)  # Initialize Fernet with the key

    while True:
        message = input(f"Hi {cs(username.title(), 'cyan')}, enter a message you want to encrypt (or type 'done' to finish): ")
        if message.lower() == 'done':
            break
        message += f"\n\nMessage created at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        messages.append(fernet.encrypt(message.encode()).decode('utf-8'))  # Encrypt and add the message to the list

    # Store username, password, messages, and key in the credentials dictionary
    credentials = {
        'username': username,
        'password': hashed_password,  # Store the hashed password
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
    global decrypted, username, password, fernet, data  # Define these variables as global
    load_user_data()  # Ensure data is loaded before login
    while not decrypted:
        name_input = input("What's your name? ")
        for user in data:
            if user['username'].lower() == name_input.lower() and not decrypted:  # Check if the username exists in the data (case-insensitive)
                while True:  # Keep asking for the password until the correct one is entered
                    time.sleep(2)
                    password_input = input(f"Hello, {username}. Please enter your password: ")
                    hashed_password = user['password']
                    if bcrypt.check_password_hash(hashed_password, password_input):  # Check if the password is correct
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

def logout(): # Function to log out the user
    global fernet, username
    fernet = None
    username = ""
    print("You have been logged out.")

def display_messages(): # Function to display messages
    global username, data, fernet
    if not fernet:
        print("You need to log in first to access your messages.")
        return

    for user in data: # Find the user in the data
        if user['username'].lower() == username.lower():
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
    global username, data, fernet
    if not fernet: # Check if the user is logged in
        print("You need to log in first to add a message.")
        return

    new_message = input("Enter the message you want to add: ")
    new_message += f"\n\nMessage created at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    for user in data: # Find the user in the data
        if user['username'].lower() == username.lower():
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

#======================================================================================================
# This is where the program starts. Registration and login functions are called here.
def program():
    global fernet
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
            register()

        elif choice == 'display messages' or choice == '3':
            clear()
            display_messages()

        elif choice == 'add message' or choice == '4':
            clear()
            add_message()

        elif choice == 'logout' or choice == '5':
            clear()
            logout()

        elif choice == 'exit' or choice == '6':
            clear()
            print(cs("Exiting program", "magenta"))
            time.sleep(2)
            exit()


# Call the program function to start the program
program()


