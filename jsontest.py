import time 
import os 
from cryptography.fernet import Fernet 
from stringcolor import cs 
import datetime
import json

clear = lambda: os.system('clear') 
clear() 


decrypted = False 


username = ""
password = ""
message = ""
creation_time = ""
credentials = {}

FILE_PATH = './users.json'



def register():
    global username, password, fernet, creation_time  
    
    username = input(cs("Enter your name: ", "cyan"))
    password = input(cs("Enter a password: ", "cyan"))
    message = input(f"Hi {cs(username.title(), 'cyan')}, enter the message you want to encrypt: ")
    creation_time = str(datetime.datetime.now().replace(microsecond=0)) 
    
    
    key = Fernet.generate_key()
    fernet = Fernet(key)  
    
    
    encMessage = fernet.encrypt(message.encode())
    encMessage_str = encMessage.decode('utf-8')
    
    
    credentials['username'] = username
    credentials['password'] = password
    credentials['message'] = encMessage_str
    credentials['key'] = key.decode('utf-8')  
    credentials['creation_time'] = creation_time
    
    
    if os.path.exists(FILE_PATH) and os.stat(FILE_PATH).st_size != 0:
        with open(FILE_PATH, 'r') as input_file:
            data = json.load(input_file)
            if isinstance(data, dict):  
                data = [data]
    else:
        data = []  
    
    data.append(credentials)  
    
    
    with open(FILE_PATH, 'w') as output_file:
        json.dump(data, output_file, indent=2)
        
    
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



def decryption(fernet, encMessage_str):
    encMessage = bytes(encMessage_str, 'utf-8')
    decMessage = fernet.decrypt(encMessage).decode()
    print("decrypted string: ", decMessage)

def login():
    global decrypted, username, password
    while not decrypted:
        # reload json file to access new user data we might have created in the same session
        with open(FILE_PATH, 'r') as input_file:
            data = json.load(input_file)
        name_input = input("What's your name? ")
        for user in data:
            if user['username'] == name_input and not decrypted:
                while True: 
                    time.sleep(2)
                    password_input = input(f"Hello, {username}. Please enter your password: ")
                    if user['password'] == password_input:
                        time.sleep(2)
                        print("Message created at:", user['creation_time'])
                        time.sleep(1)
                        fernet = Fernet(user['key'])  
                        decrypted = True
                        decryption(fernet, user['message'])  
                        
                        break
                    else:
                        time.sleep(2)
                        print("This is not the password >:(")
            break





print("Welcome to the encryptian program. \n")
time.sleep(1)



while True:  
    choice = input("Would you like to register or login? (register/login) \n")
    
    if choice.lower() == 'login': 
        login()
        break  
    
    elif choice.lower() == 'register': 
        register()
        break  
    
    else:
        print("Invalid choice. Please enter either 'login' or 'register'.")