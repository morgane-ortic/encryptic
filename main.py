import time # import the time library that we will use lter in the code
import os # import the os library
from cryptography.fernet import Fernet # import fernet from the cryptography library, used for encryption and decryption
from stringcolor import cs # import cs from the stringcolor library
import json

clear = lambda: os.system('clear') # define a "clear" function that clears the terminal from previous lines
clear() # call the clear function to clear the terminal

#Global variables
decrypted = False # define that the decryption process hasn't happened yet.
# create empty variables that we will use to store the values we define later
# It's not necessary in this code, but it's good practice and helps with readability
username = ""
password = ""
message = ""
credentials = {}

FILE_PATH = './users.json'

# Functions
# Register a new user, password and message and encrypts the message:
def register():
    global username, password, encMessage, fernet # define these values as global, so that they are stored + can be used outside the function

    #asks user for username, password and message and stores them in the variables created earlier
    username = input(cs("Enter your name: ", "cyan"))
    password = input(cs("Enter a password: ", "cyan"))
    message = input(f"Hi {cs(username.title(), 'cyan')}, enter the message you want to encrypt: ")
    
    key = Fernet.generate_key() # generate a key for encryption and decryption using fernet
    fernet = Fernet(key) # Instance the Fernet class with the key
    # then use the Fernet class instance to encrypt the string
    # string must be encoded to byte string before encryption
    # store encoded message as a string in encMessage variable
    encMessage = fernet.encrypt(message.encode())
    # stores username and password to the credentials list we created earlier

    credentials['username'] = username
    credentials['password'] = password

    # Check if the file exists and is not empty
    if os.path.exists(FILE_PATH) and os.stat(FILE_PATH).st_size != 0:
        with open(FILE_PATH, 'r') as input_file:
            data = json.load(input_file)
            # If data is a dictionary, convert it to a list
            if isinstance(data, dict):
                data = [data]
            data.append(credentials)
    else:
        # If the file doesn't exist or is empty, start a new list
        data = [credentials]

    # Write the data to the file
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
def decryption():
    decMessage = fernet.decrypt(encMessage).decode() # decrypt message and stores it in clear in decMessage variable
    print("decrypted string: ", decMessage) # print decrypted string

# Login as a registered user to decrypt message
def login():
    global decrypted
    while decrypted == False: # keep asking this input until messge is decrypted
        name_input = input("What\'s your name? ") # ask for username
        if name_input == username and decrypted == False: # if name is correct, keep asking this until message is decrypted
            while True: 
                time.sleep(2)
                password_input = input(f"Hello, {username}. Please enter your password: ") # ask for password
                if password_input == password:
                    time.sleep(2)
                    decrypted = True # define that the message is decrypted = stop asking for username
                    decryption() # call decryption function that decrypts message
                    break
                # If password is wrong, print an error message
                else:
                    time.sleep(2)
                    print("This is not the password >:(")



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