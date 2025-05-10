from cryptography.fernet import Fernet

# Load the key from secret.key file
def load_key():
    with open("secret.key", "rb") as key_file:
        return key_file.read()

key = load_key()
fernet = Fernet(key)

# Encrypt a string and return bytes
def encrypt_data(data):
    return fernet.encrypt(data.encode())

# Decrypt encrypted bytes (optional, for reading logs)
def decrypt_data(encrypted_data):
    return fernet.decrypt(encrypted_data).decode()
