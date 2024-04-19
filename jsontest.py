import time # import the time library that we will use lter in the code
import os # import the os library
from cryptography.fernet import Fernet # import fernet from the cryptography library, used for encryption and decryption
from stringcolor import cs # import cs from the stringcolor library
import json
from flask_bcrypt import Bcrypt

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
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') # Hash the password
    message = input(f"Hi {cs(username.title(), 'cyan')}, enter the message you want to encrypt: ")
    
    # Generate a key for encryption and decryption using Fernet
    key = Fernet.generate_key()
    fernet = Fernet(key)  # Initialize Fernet with the key
    
    # Encrypt the message
    encMessage = fernet.encrypt(message.encode())
    encMessage_str = encMessage.decode('utf-8')
    
    # Store username, password, message, and key in the credentials dictionary
    credentials['username'] = username
    credentials['password'] = hashed_password
    credentials['message'] = encMessage_str
    credentials['key'] = key.decode('utf-8')  # Convert the key to a string and store it
    
    # Load existing data from the JSON file
    if os.path.exists(FILE_PATH) and os.stat(FILE_PATH).st_size != 0:
        with open(FILE_PATH, 'r') as input_file:
            data = json.load(input_file)
            if isinstance(data, dict):  # If data is a dictionary, convert it to a list
                data = [data]
    else:
        data = []  # If the file doesn't exist or is empty, start with an empty list
    
    data.append(credentials)  # Append the new credentials to the list
    
    # Write the data back to the JSON file
    with open(FILE_PATH, 'w') as output_file:
        json.dump(data, output_file, indent=2)
        
    
    clear() # clear the terminal
    print("Registration successful! \n") # let user know registration worked
    time.sleep(2) # give a 2 seconds break before next line
    clear() # clear the terminal
    # Loading screen redirecting to login function
    print("You can now login with your new account. \n")
    print("Redirecting to login page", end='', flush=True) # display text letter by letter
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

def login():
    global decrypted, username, password, fernet
    with open(FILE_PATH, 'r') as input_file:
        data = json.load(input_file)
    while not decrypted:
        name_input = input("What's your name? ")
        for user in data:
            if user['username'] == name_input and not decrypted:
                while True: 
                    time.sleep(2)
                    password_input = input(f"Hello, {username}. Please enter your password: ")
                    hashed_password = user['password']
                    if bcrypt.check_password_hash(hashed_password, password_input):
                        time.sleep(2)
                        fernet = Fernet(user['key'])  # Initialize Fernet with the user's key
                        decrypted = True
                        decryption(fernet, user['message'])  # Pass the fernet instance and the encrypted message to decryption function
                        break
                    else:
                        time.sleep(2)
                        print("This is not the password >:(")
            break



#======================================================================================================
# This is where the program starts. Registration and login functions are called here.
print("Welcome to the encryptian program. \n")
time.sleep(1)

# Ask the user if they want to register or login
# calling functions Register or Login accordingly
while True:  # keep asking until a valid choice is given
    choice = input("Would you like to register or login? (register/login) \n")
    # call login function if login is typed
    if choice.lower() == 'login': # use lower method so it accepts login with different capitalisation
        login()
        break  # exit the loop once a valid choice is given
    # call register function if register is typed
    elif choice.lower() == 'register': # 
        register()
        break  # exit the loop once a valid choice is given
    # print error message if user enters something else
    else:
        print("Invalid choice. Please enter either 'login' or 'register'.")