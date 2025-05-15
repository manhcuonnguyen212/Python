from cryptography.fernet import Fernet
import os

# Generate an encryption key
def generate_key():
    key = Fernet.generate_key()
    with open("encryption_key.key", "wb") as key_file:
        key_file.write(key)

# Load the encryption key
def load_key():
    return open("encryption_key.key", "rb").read()

# Encrypt files in a folder
def encrypt_files(folder_path):
    key = load_key()
    fernet = Fernet(key)

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)

            with open(file_path, "rb") as f:
                file_data = f.read()
            encrypted_data = fernet.encrypt(file_data)

            with open(file_path, "wb") as f:
                f.write(encrypted_data)

            print(f"Encrypted: {file_path}")

# Safe execution in a test directory
generate_key()
encrypt_files("D:\\TOÁN RỜI RẠC\\TOÁN RỜI RẠC")  # Change this to a safe folder
