
# Password Encryption Script

This Python script provides functionality to securely encrypt and decrypt passwords using the `cryptography` library. The script includes functions for creating an encryption key, encrypting a password, and decrypting it later. 

## Features

- **Create and Save Encryption Key**: Generates an encryption key and saves it to a specific location on your filesystem.
- **Encrypt Password**: Encrypts a password provided by the user and saves it to a specified file.
- **Decrypt Password**: Decrypts the password from the encrypted file using the saved encryption key.
- **Default Arguments**: Provides functions with default paths for encryption key and password storage locations.

## Installation

Before using the script, you need to install the `cryptography` library. You can do this via pip:

```bash
pip install cryptography
```

## Usage

### 1. Creating the Encryption Key

The `create_encryption_key` function generates a new encryption key and saves it to a specified location. If no location is specified, the key is saved to the default location.

#### Example:

```python
from your_script import create_encryption_key

# Create and save the encryption key
key_path = create_encryption_key()
```

By default, the key is saved to:

```
C:\Users\{username}\My Documents\Python\Encrypted Keys\password_encryption.key
```

If the directory does not exist, it will be created.

### 2. Encrypting the Password

The `encrypt_and_store_password` function asks the user for a password, encrypts it using the provided encryption key, and then saves the encrypted password to a file.

#### Example:

```python
from your_script import encrypt_and_store_password

# Encrypt the password and store it
encrypt_and_store_password(key_path)
```

By default, the encrypted password is saved to:

```
H:\encrypted_password.txt
```

### 3. Decrypting the Password

The `decrypt_password` function decrypts the password stored in the file using the provided encryption key.

#### Example:

```python
from your_script import decrypt_password

# Decrypt the password
decrypted_password = decrypt_password(key_path, "H:\encrypted_password.txt")
```

The decrypted password will be printed to the console.

### 4. Using Default Arguments

For convenience, two functions are provided with default arguments for the encryption key location and password storage location:

- **`encrypt_password_with_defaults`**: Uses default paths to create an encryption key (if it doesn't exist), encrypt the password, and store it.

```python
from your_script import encrypt_password_with_defaults

# Encrypt and store the password using default paths
encrypt_password_with_defaults()
```

- **`decrypt_password_with_defaults`**: Uses default paths to load the encryption key, decrypt the password, and print it.

```python
from your_script import decrypt_password_with_defaults

# Decrypt the password using default paths
decrypt_password_with_defaults()
```

## Conclusion

This script is designed to help you securely encrypt and decrypt passwords in Python. It is flexible enough to allow custom paths but also provides default locations for ease of use. Ensure that the encryption key is stored securely, as anyone with access to it can decrypt your passwords.
