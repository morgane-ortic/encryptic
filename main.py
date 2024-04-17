import time
import os
from cryptography.fernet import Fernet
from stringcolor import cs

clear = lambda: os.system('clear')
clear()

#Global variables
decrypted = False
username = ""
password = ""
message = ""
credentials = []

# Functions:
# Function to register a new account
def register():
    global username, password, message

    username = input(cs("Enter a new username: ", "cyan")) 
    password = input(cs("Enter a new password: ", "cyan"))   
    clear()
    message = input(f"Hi {cs(username.title(), 'cyan')}, enter the message you want to encrypt: ")
    clear()
    encryption()
    print("Encrypting: ", end='', flush=True) 
    print(show_letters(encMessage))       # print the encrypted string
    time.sleep(2)
    credentials.append(username) # Store the username and password in a list
    credentials.append(password)
    clear()
    print("Registration successful! \n")
    time.sleep(2)
    clear()
    print("You can now login with your new account. \n")
    print("Redirecting to login page", end='', flush=True)
    print(show_letters('..........'), end='', flush=True)
    time.sleep(1)
    clear()
    login()

# Function to login
def login():
    global decrypted
    while decrypted == False:
        name_input = input("What\'s your name? ")
        clear()
        if name_input == username and decrypted == False:
            while True: 
                password_input = input(f"Hello, {cs(username.title(), 'cyan')}. Please enter your password: ")
                name_given = True
                clear()
                print("Loading encrypted message", end='', flush=True)
                print(show_letters('..........'), end='', flush=True)
                if password_input == password:
                    decrypted = True
                    decryption()
                    break 
                else:
                    time.sleep(2)
                    print("This is not the password >:()")
        if name_input != username:
            print("Non-existent username >:()")
            print("\nWould you like to register? (yes/no)")
            if input() == 'yes':
                print("Redirecting to registration page", end='', flush=True)
                clear()
                register()
            else:
                clear()
                print("Try logging in again.\n")
                login()
                
# Function to encrypt the message
def encryption():
    global encMessage, fernet, message
    key = Fernet.generate_key()     # Using Fernet to generate a key (any other key generator could be used as well)
    fernet = Fernet(key)            # We tell the Fernet class to use the key we generated
    encMessage = fernet.encrypt(message.encode()) # Encrypt the message / to encrypt the string it must be encoded to byte string before encryption

# Function to decrypt the message
def decryption():                                    
    decMessage = fernet.decrypt(encMessage).decode() # decrypting the encrypted string with the same Fernet instance that was used for encrypting the string
    clear()                                          # encoded byte string is returned by decrypt method, so decode it to string with decode methods
    print("decrypted string: ", decMessage)          # print the decrypted string

# Function to show the letters one by one
def show_letters(string):
    for char in string:
        time.sleep(0.03)
        print(char, end=' ', flush=True)
    return ''
        
#======================================================================================================
# This is where the program starts. Registration and login functions are called here.
print("Welcome to the encryptian program. \n")
time.sleep(1)

choice = input('Would you like to register or login? (register/login) \n', )
while choice != 'register' or 'login':
    if choice == 'register':
        clear()
        register()
        break
    elif choice == 'login':
        clear()
        login()
        break

