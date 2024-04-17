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


# Functions
# Function to register a new account
def register():
    global username, password, encMessage, fernet

    username = input(cs("Enter your name: ", "cyan"))
    password = input(cs("Enter a password: ", "cyan"))
    message = input(f"Hi {cs(username.title(), 'cyan')}, enter the message you want to encrypt: ")
    
# generate a key for encryption and decryption
# You can use fernet to generate 
# the key or use random key generator
# here using fernet to generate key
    key = Fernet.generate_key()
# Instance the Fernet class with the key
    fernet = Fernet(key)
# then use the Fernet class instance 
# to encrypt the string string must
# be encoded to byte string before encryption
    encMessage = fernet.encrypt(message.encode())
    credentials.append(username)
    credentials.append(password)
    clear()
    print("Registration successful! \n")
    time.sleep(2)
    clear()
    print("You can now login with your new account. \n")
    print("Redirecting to login page", end='', flush=True)
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

# decrypt the encrypted string with the 
# Fernet instance of the key,
# that was used for encrypting the string
# encoded byte string is returned by decrypt method,
# so decode it to string with decode methods
def decryption():
    decMessage = fernet.decrypt(encMessage).decode()
    print("decrypted string: ", decMessage)

def login():
    global decrypted
    while decrypted == False:
        name_input = input("What\'s your name? ")
        if name_input == username and decrypted == False:
            while True:  # added this line
                time.sleep(2)
                password_input = input(f"Hello, {username}. Please enter your password: ")
                name_given = True
                if password_input == password:
                    time.sleep(2)
                    decrypted = True
                    decryption()
                    break  # added this line
                else:
                    time.sleep(2)
                    print("This is not the password >:()")



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

