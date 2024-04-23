import time                             #imports the time module, which allows us to use functions with time                
import os                               #imports the os module, which allows us to use functions that interact with the operating system
from cryptography.fernet import Fernet  #imports the Fernet class from the cryptography module, which allows us to encrypt and decrypt data
from stringcolor import cs              #imports the stringcolor module, which allows us to use colors in the terminal                    
# import mysql.connector                #imports the required function that allows Python to connect to MySQL. / Currently not used


#======================================================================================================
#Global variables
usernames = ""
passwords = ""
messages = ""
credentials = {}
credentials1 = []
key = Fernet.generate_key()
fernet = Fernet(key)

#======================================================================================================
# Functions::

clear = lambda: os.system('clear') # define a "clear" function that clears the terminal from previous lines
clear() # call the clear function to clear the terminal

# Function that works as the main menu of the program (logical part of the main menu)
def main_menu_logic():
    main_menu_ui()
    main_menu_choice = ""
    while main_menu_choice != 'login' or 'register' or 'exit' or '1' or '2' or '3':
        choice = input("Enter your choice: ").lower()
        clear()
        main_menu_ui()
        if choice == 'login' or choice == '1':
            clear()
            loging_in()
            logged_in_menu_logic()
        elif choice == 'register' or choice == '2':
            clear()
            register_account()
        elif choice == 'exit' or choice == '3':
            clear()
            print(cs("Exiting program", "magenta") , end='', flush=True)
            print(print_letters_appart(20 * '.'))
            time.sleep(0.5)
            clear()
            exit()
        break

# Function that shows the main menu choices - User Interface (Graphical part of the main menu)
def main_menu_ui():
    print(cs("Welcome to the encryptian program. \n" , "blue"))
    print("╔" + "═" * 14 + "╗")
    print("║ 1. Login     ║" , "\n║ 2. Register  ║" , "\n║ 3. Exit      ║")
    print("╚" + "═" * 14 + "╝\n")

# Function that lets you register a new account
def register_account():
    global messages, usernames, passwords
    usernames = input(cs("Enter a new username: ", "cyan"))
    passwords = input(cs("Enter a new password: ", "cyan"))   
    credentials1.append(usernames)
    credentials1.append(passwords)
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
            # insert_info_in_database() MySQL database function / not in use but works
            time.sleep(0.5)
            print(cs("\nMessage added!" , "yellow"))
            break
        elif initial_message == 'no' and initial_message != 'yes':
            clear()
            break
        else:
            clear()
            print("Would you like to input an initial message or not?.")
    print(cs("\nRegistration successful!" , "yellow"))
    time.sleep(2)
    clear()
    print(cs("Redirecting to main menu", "orange"), end='', flush=True)
    print(print_letters_appart(20 * '.'))
    clear()
    print("You can now login with your new account. ")
    time.sleep(3)
    clear()
    main_menu_logic()

# Function that lets you login to your account
def loging_in():
    global usernames, passwords
    while True:
        name_input = input(cs("Enter your username: ", "cyan"))
        if not name_input.strip():
            print("Username cannot be blank. Please try again.")
            time.sleep(1)
            clear()
            continue
        elif name_input != usernames:
            print(cs("Non-existent username >:()", "red"))
            print("\nWould you like to register? (yes/no)")
            if input().lower() == 'yes':
                print("Redirecting to registration page", end='', flush=True)
                clear()
                register_account()
            else:
                clear()
                main_menu_logic()

        passwords_input = input(cs("Enter your password: ", "cyan"))
        if not passwords_input.strip():
            print("Password cannot be blank. Please try again.")
            time.sleep(1)
            clear()
            continue
        elif passwords_input != passwords:
            print(cs("Incorrect password >:()", "red"))
            loging_in()
        else:
            print(cs("Logging in", "yellow"), end='', flush=True)
            print(print_letters_appart(20 * '.'))
            time.sleep(0.5)
            clear()
            break

# Function that shows the choices after logging in - User Interface (Graphical part after logging in)
def logged_in_menu_ui():
    print(cs("Welcome to the encryptian program. \n" , "blue"))
    print(cs(f"Logged in as: {usernames.title()}\n", "cyan"))
    print("╔" + "═" * 22 + "╗")
    print("║ 1. Display message   ║" , "\n║ 2. Add Message       ║" , "\n║ 3. Delete Message    ║")
    print("║ 4. Log Out           ║" , "\n║ 5. Exit              ║")
    print("╚" + "═" * 22 + "╝\n")

# Function that works as the functional part of the program after logging in (Logical part after logging in)
def logged_in_menu_logic():
    logged_in_menu_ui()
    global messages, encMessages, decMessages
    logged_in_choice = input("Enter your choice: ").lower()
    while (logged_in_choice != 'display message' or 'add message' or 'delete message' or 
           'log out' or 'exit' or '1' or '2' or '3' or '4' or '5'):
        if logged_in_choice == 'display message' or logged_in_choice == '1':
            clear()
            decryption_function()
            print(cs("Decrypting: ", " green"), end='', flush=True)
            print(print_letters_appart(decMessages))
            time.sleep(2)
            clear()
            logged_in_menu_logic()
            break
        elif logged_in_choice == 'add message: ' or logged_in_choice == '2':
            clear()
            print(cs("Enter a new message: ", "cyan"), end='', flush=True )
            messages = input()
            encryption_function()
            print(cs("Encrypting: ", "green"), end='', flush=True) 
            print(print_letters_appart(encMessages))
            # insert_info_in_database() MySQL database function / not in use but it works
            time.sleep(2)
            clear()
            logged_in_menu_logic()
            break
        elif logged_in_choice == 'delete message' or logged_in_choice == '3':
            clear()
            print(cs("Deleting message", "magenta"), end='', flush=True)
            print(print_letters_appart(20 * '.'))
            time.sleep(1.5)
            clear()
            messages = ""
            print(cs("Message deleted", "yellow"), end='', flush=True)
            print(print_letters_appart(20 * '.'))
            time.sleep(1.5)
            clear()
            logged_in_menu_logic()
            break
        elif logged_in_choice == 'log out' or logged_in_choice == '4':
            clear()
            print(cs("Logging out", "magenta"), end='', flush=True)
            print(print_letters_appart(20 * '.'))
            time.sleep(0.5)
            clear()
            print(cs("Redirecting to main menu", "orange"), end='', flush=True)
            print(print_letters_appart('..........\n\n'))
            clear()
            main_menu_logic()
        elif logged_in_choice == 'exit' or logged_in_choice == '5':
            clear()
            print(cs("Exiting program", "magenta") , end='', flush=True)
            print(print_letters_appart(20 * '.'))
            time.sleep(1.5)
            clear()
            exit()

        

# Function that encrypts the message inputed by the user
def encryption_function():
    global encMessages, key
    key = Fernet.generate_key()     # Using Fernet to generate a key (any other key generator could be used as well)
    fernet = Fernet(key)            # We tell the Fernet class to use the key we generated
    encMessages = fernet.encrypt(messages.encode()) # Encrypt the messages / to encrypt the string it must be encoded to byte string before encryption_function

# Function that decrypts an encrypted message
def decryption_function():  
    global decMessages, key
    key = Fernet.generate_key() # Using Fernet to generate a key (any other key generator could be used as well)                  
    fernet = Fernet(key) # We tell the Fernet class to use the key we generated
    decMessages = fernet.decrypt(encMessages).decode() # decrypting the encrypted string with the same Fernet instance that was used for encrypting the string

# Function that prints out string characters one by one
def print_letters_appart(string):
    for char in string:
        time.sleep(0.03)
        print(char, end=' ', flush=True)
    return '' 

# Working with MySQL database / Not in use but it would work if uncommented         
'''
# Function that inserts the user data and message into the database
def insert_info_in_database():
    global usernames, passwords, encMessages
    mydb = mysql.connector.connect( #The mydb section configures the information for the database.
        host="localhost",
        user="roger",
        password="123",
        database="Warfare_encryption_function_Tool"
    )

    mycursor = mydb.cursor() # mydb.cursor() is the function that allows the insertion of data into the database.
 
    sql = "INSERT INTO user_accounts (usernames, passwords, messages) VALUES (%s, %s, %s)" # The sql line is our first MySQL query.
    val = (usernames, passwords, encMessages)                                                 # The val line defines our columns for the database.
    mycursor.execute(sql, val)                                                             # The mycursor.execute executes the above operations.
    mydb.commit()                                                                          # The mydb.commit() confirms the changes made by mycursor.execute. 
    print(cs("Uploading encrypted message:" , "yellow"), end='', flush=True)
    print(cs(30 * '.' , "yellow"), end='', flush=True)
    clear()
    print(mycursor.rowcount, "Record uploaded.") # The print line prints output to indicate success or failure.
    
# Function that retrieves the data from the database / not yet implemented
def retrieve_info_from_database():
    mydb = mysql.connector.connect(
    host="localhost",
    user="roger",
    password="123",
    database="Warfare_encryption_function_Tool"
    )

    mycursor.execute("SELECT * FROM table_name WHERE condition")
    
    # Fetch the result
    mycursor = mydb.cursor() # mydb.cursor() is the function that allows the insertion of data into the database.
    result = mycursor.fetchall()
    
    # Process the result
    for row in result:
        print(row)
'''

#======================================================================================================
# This is where the program starts.

main_menu_logic()