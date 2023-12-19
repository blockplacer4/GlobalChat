from cryptography.fernet import Fernet

# Create a Fernet object
fernet = Fernet.generate_key()

# Encrypt a message
message = ""
encrypted_message = fernet.encrypt(message.encode('utf-8'))
print(encrypted_message)

# Decrypt the message
decrypted_message = fernet.decrypt(encrypted_message).decode('utf-8')
print(decrypted_message)

import cryptography.fernet as fernet

def save_fernet_key(key, filename):
    with open(filename, 'wb') as f:
        f.write(key.encode())

def load_fernet_key(filename):
    with open(filename, 'rb') as f:
        key = f.read()
        return fernet.Fernet(key)

