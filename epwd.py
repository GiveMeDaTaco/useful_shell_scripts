import os
from cryptography.fernet import Fernet
import getpass

def create_encryption_key(file_path=None):
    if file_path is None:
        file_path = os.path.join(os.path.expanduser("~"), "My Documents", "Python", "Encrypted Keys", "password_encryption.key")
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Generate the key and save it
    key = Fernet.generate_key()
    with open(file_path, 'wb') as key_file:
        key_file.write(key)
    
    print(f"Encryption key saved to {file_path}")
    return file_path

def encrypt_and_store_password(key_path, password_file_path=None):
    if password_file_path is None:
        password_file_path = "H:\\\\encrypted_password.txt"
    
    # Load the encryption key
    with open(key_path, 'rb') as key_file:
        key = key_file.read()
    
    cipher_suite = Fernet(key)
    
    # Ask for the user's password
    password = getpass.getpass("Enter the password to encrypt: ")
    
    # Encrypt the password
    encrypted_password = cipher_suite.encrypt(password.encode())
    
    # Store the encrypted password
    with open(password_file_path, 'wb') as file:
        file.write(encrypted_password)
    
    print(f"Encrypted password saved to {password_file_path}")
    return password_file_path

def decrypt_password(key_path, encrypted_password_file):
    # Load the encryption key
    with open(key_path, 'rb') as key_file:
        key = key_file.read()
    
    cipher_suite = Fernet(key)
    
    # Load the encrypted password
    with open(encrypted_password_file, 'rb') as file:
        encrypted_password = file.read()
    
    # Decrypt the password
    decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
    
    print(f"Decrypted password: {decrypted_password}")
    return decrypted_password

def encrypt_password_with_defaults():
    # Default paths
    key_path = os.path.join(os.path.expanduser("~"), "My Documents", "Python", "Encrypted Keys", "password_encryption.key")
    password_file_path = "H:\\\\encrypted_password.txt"
    
    # Create the key if it doesn't exist
    if not os.path.exists(key_path):
        create_encryption_key(key_path)
    
    # Encrypt and store the password
    encrypt_and_store_password(key_path, password_file_path)

def decrypt_password_with_defaults():
    # Default paths
    key_path = os.path.join(os.path.expanduser("~"), "My Documents", "Python", "Encrypted Keys", "password_encryption.key")
    encrypted_password_file = "H:\\\\encrypted_password.txt"
    
    # Decrypt the password
    decrypt_password(key_path, encrypted_password_file)
