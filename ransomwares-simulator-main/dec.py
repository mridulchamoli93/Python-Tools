from cryptography.fernet import Fernet
import os

key = b'eySY2FUxQZW1yT7PlpcaAO2HdvdJcbiNAgejJBuDvN8='

def decrypt_file():
    current_directory = os.getcwd()
    cipher = Fernet(key)
    
    for root, dirs, files in os.walk(current_directory):
        for file_name in files:
            if file_name.endswith(".txt"):
                file_path = os.path.join(root, file_name)
                
                with open(file_path, "rb") as f:
                    encrypted_data = f.read()
                    
                # Decrypt the file content
                decrypted_data = cipher.decrypt(encrypted_data)
                
                with open(file_path, "wb") as f:
                    f.write(decrypted_data)