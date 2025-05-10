from cryptography.fernet import Fernet
import os
    
def load_key():
    return open("encryption_key.key", "rb").read()

def decrypt_files(folder_path):
    key = load_key()
    fernet = Fernet(key)

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)

            with open(file_path, "rb") as f:
                encrypted_data = f.read()
            decrypted_data = fernet.decrypt(encrypted_data)

            with open(file_path, "wb") as f:
                f.write(decrypted_data)

            print(f"Decrypted: {file_path}")

# Decrypt the test folder
decrypt_files("D:\\TOÁN RỜI RẠC\\TOÁN RỜI RẠC")
