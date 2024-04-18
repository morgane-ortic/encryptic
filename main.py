import time                             #imports the time module, which allows us to use functions with time                
import os                               #imports the os module, which allows us to use functions that interact with the operating system
from cryptography.fernet import Fernet  #imports the Fernet class from the cryptography module, which allows us to encrypt and decrypt data
from stringcolor import cs              #imports the stringcolor module, which allows us to use colors in the terminal                    
import mysql.connector                  #imports the required function that allows Python to connect to MySQL.

clear = lambda: os.system('clear') # define a "clear" function that clears the terminal from previous lines
clear() # call the clear function to clear the terminal

#Global variables
decrypted = False
usernames = ""
passwords = ""
messages = ""
credentials = []

#======================================================================================================
# Functions::
# Function that lets you register a new account
def register():
    global usernames, passwords, messages

    usernames = input(lower(cs("Enter a new username: ", "cyan")) )
    passwords = input(cs("Enter a new password: ", "cyan"))   
    clear()
    messages = input(f"Hi {cs(usernames.title(), 'cyan')}, enter the message you want to encrypt: ")
    clear()
    encryption()
    print(cs("Encrypting: ", "green"), end='', flush=True) 
    print(show_letters(encMessages))       # print the encrypted string
    time.sleep(2)
    credentials.append(usernames) # Stores the usernames and passwords in a list
    credentials.append(passwords)
    clear()
    print(cs("Registration successful!" , "yellow"))
    time.sleep(2)
    clear()
    print(cs("Redirecting to login", "orange"), end='', flush=True)
    print(show_letters('..........\n\n'), end='', flush=True)
    print("You can now login with your new account. ")
    time.sleep(3)
    clear()
    login()

# Function that lets you login to your account
def login():
    global decrypted
    while decrypted == False:
        name_input = input(cs("Enter your username: " , "cyan"))
        clear()
        if name_input == usernames and decrypted == False:
            while True: 
                passwords_input = input(f"Hello, {cs(usernames.title(), 'cyan')}. Please enter your passwords: ")
                name_given = True
                clear()
                print("Loading encrypted message", end='', flush=True)
                print(show_letters('..........'), end='', flush=True)
                if passwords_input == passwords:
                    decrypted = True
                    decryption()
                    break 
                else:
                    time.sleep(2)
                    print(cs("This is not the password >:()", "red"))
        if name_input != usernames:
            print(cs("Non-existent username >:()", "red"))
            print("\nWould you like to register? (yes/no)")
            if input() == 'yes':
                print("Redirecting to registration page", end='', flush=True)
                clear()
                register()
            else:
                clear()
                print("Try logging in again.\n")
                login()
                
# Function that encrypts the message inputed by the user
def encryption():
    global encMessages, fernet, messages
    key = Fernet.generate_key()     # Using Fernet to generate a key (any other key generator could be used as well)
    fernet = Fernet(key)            # We tell the Fernet class to use the key we generated
    encMessages = fernet.encrypt(messages.encode()) # Encrypt the messages / to encrypt the string it must be encoded to byte string before encryption

# Function that takes the encrypted message and decrypts it
def decryption():                                    
    global decMessages
    decMessages = fernet.decrypt(encMessages).decode() # decrypting the encrypted string with the same Fernet instance that was used for encrypting the string
    clear()                                            # encoded byte string is returned by decrypt method, so decode it to string with decode methods

# Function that shows string characters one by one
def show_letters(string):
    for char in string:
        time.sleep(0.03)
        print(char, end=' ', flush=True)
    return ''
        
# Function that connects to the database and inserts the data
def insert_info_in_database():
    mydb = mysql.connector.connect( #The mydb section configures the information for the database.
    host="localhost",
    user="roger",
    password="123",
    database="Warfare_Encryption_Tool"
    )

    mycursor = mydb.cursor() # mydb.cursor() is the function that allows the insertion of data into the database.
 
    sql = "INSERT INTO user_accounts (usernames, passwords, messages) VALUES (%s, %s, %s)" # The sql line is our first MySQL query.
    val = (usernames, passwords, encMessages)                                                 # The val line defines our columns for the database.
    mycursor.execute(sql, val)                                                             # The mycursor.execute executes the above operations.
    mydb.commit()                                                                          # The mydb.commit() confirms the changes made by mycursor.execute. 
    print("Uploading encrypted message:", end='', flush=True)
    print(show_letters('.................'), end='', flush=True)
    print(mycursor.rowcount, "\nRecord uploaded.") # The print line prints output to indicate success or failure.
    
# Function that retrieves the data from the database
def retrieve_info_from_database():
    mydb = mysql.connector.connect(
    host="localhost",
    user="roger",
    password="123",
    database="Warfare_Encryption_Tool"
    )

    mycursor.execute("SELECT * FROM table_name WHERE condition")
    
    # Fetch the result
    mycursor = mydb.cursor() # mydb.cursor() is the function that allows the insertion of data into the database.
    result = mycursor.fetchall()
    
    # Process the result
    for row in result:
        print(row)
#======================================================================================================
# This is where the program starts. Registration and login functions are called here.
print(cs("Welcome to the encryptian program. \n" , "blue"))
time.sleep(1)

# Ask the user if they want to register or login / calling functions Register and Login
print(' 1. Login \n' , '2. Register \n' , '3. Exit \n')
choice = input("Enter your choice: ").lower()
while choice != 'login' or 'register' or 'exit' or '1' or '2' or '3':
    if choice == 'login' or choice == '1':
        clear()
        login()
        print(' 1. Log out \n' , '2. Enter a message \n' , '3. Exit \n')
        choice2 = input("What would you like to do? \n")
        while
        



        break
    elif choice == 'register' or choice == '2':
        clear()
        register()
        break
    elif choice == 'exit' or choice == '3':
        clear()
        print(cs("Exiting program", "magenta"))
        time.sleep(2)
        exit()



insert_info_in_database()

