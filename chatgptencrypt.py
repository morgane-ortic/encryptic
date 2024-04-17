import hashlib
from cryptography.fernet import Fernet
from stringcolor import cs

# Function to create a new user account
def create_user(username, password):
    # Hash the password
    hashed_password = hash_password(password)
    # Store username and hashed password
    users[username] = hashed_password

def hash_password(password):
    # Convert password to bytes
    password_bytes = password.encode('utf-8')
    # Create a hash object
    hash_object = hashlib.sha256()
    # Update hash object with password bytes
    hash_object.update(password_bytes)
    # Get the hexadecimal representation of the hashed password
    hashed_password = hash_object.hexdigest()
    return hashed_password

# Function to log in and retrieve encrypted message
def login(username, password):
    username = username.lower()  # Convert username to lowercase
    if username in users:
        hashed_password = users[username]
        # Check if the hashed password matches the stored hashed password
        if verify_password(password, hashed_password):
            encrypted_message = user_messages.get(username, "")
            if encrypted_message:
                # Decrypt message and display
                decrypted_message = f.decrypt(encrypted_message).decode()
                print("Your encrypted message:", decrypted_message)
            else:
                print("No message found for this user.")
        else:
            print("Invalid password.")
    else:
        print("Invalid username.")


# Function to verify a password
def verify_password(password, hashed_password):
    # Hash the password to be verified
    hashed_password_to_verify = hash_password(password)
    # Compare the hashed passwords
    return hashed_password_to_verify == hashed_password

# Function to add a message to the user's account
def add_message(username, message):
    encrypted_message = f.encrypt(message.encode())
    user_messages[username] = encrypted_message

# Function to log in and add a message
def login_and_add_message(username, password):
    if username in users:
        hashed_password = users[username]
        if verify_password(password, hashed_password):
            message = input("Enter your message: ")
            add_message(username, message)
            print("Message added successfully.")
        else:
            print("Invalid password.")
    else:
        print("Invalid username.")


# Main program
users = {}
user_messages = {}

# Generate encryption key
key = Fernet.generate_key()
f = Fernet(key)

while True:
    print("\n1. Create Account\n2. Login\n3. Add Message\n4. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        username = input("Enter username: ")
        password = input("Enter password: ")
        create_user(username, password)

    elif choice == "2":
        username = input("Enter username: ")
        password = input("Enter password: ")
        login(username, password)

    elif choice == "3":
        username = input("Enter username: ")
        password = input("Enter password: ")
        login_and_add_message(username, password)

    elif choice == "4":
        print("Exiting program.")
        break

    else:
        print("Invalid choice. Please try again.")