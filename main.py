import time
import os

clear = lambda: os.system('clear')
clear()

#Global variables
username = ""
password = ""
credentials = []

# Functions
def register():
    username = input("Enter a new username: ")
    password = input("Enter a new password: ")
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

def login():
    username_login = input("Enter your login username: ")
    password_login = input("Enter your password: ")
    clear()
    if username_login == credentials[0] and password_login == credentials[1]:
        clear()
        print("Login successful!")
        time.sleep(2)
        print(f"\nWelcome, {username_login} !")  # Example of concatenation
        time.sleep(2)
        clear()
    else:
        print("Login failed. Please try again.")
        time.sleep(2)
        clear()
        login()


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