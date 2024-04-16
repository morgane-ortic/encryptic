from cryptography.fernet import Fernet

# we will be encrypting the below string.

name = (input("Enter your name :"))
password = (input("Enter a password :"))
message = (input(f"Hello {name}, enter the message you want to encrypt: "))

# generate a key for encryption and decryption
# You can use fernet to generate 
# the key or use random key generator
# here I'm using fernet to generate key

key = Fernet.generate_key()

# Instance the Fernet class with the key

fernet = Fernet(key)

# then use the Fernet class instance 
# to encrypt the string string must
# be encoded to byte string before encryption
encMessage = fernet.encrypt(message.encode())

# decrypt the encrypted string with the 
# Fernet instance of the key,
# that was used for encrypting the string
# encoded byte string is returned by decrypt method,
# so decode it to string with decode methods
def decryption():
    decMessage = fernet.decrypt(encMessage).decode()
    print("decrypted string: ", decMessage)

print("original string: ", message)
print("encrypted string: ", encMessage)
print("Ready for decryption")
name_input = input("What\'s your name? ")
if name_input == name:
    password_input = input(f"Hello, {name}. Please enter your password: ")
    if password_input == password:
        decryption()
    else:
        print("This is not the password >:()")
else:
    print("Sorry, again?")
