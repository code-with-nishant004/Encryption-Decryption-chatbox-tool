from cryptography.fernet import Fernet

# Generate a key (Do this once and save the key for both sender and receiver)
# key = Fernet.generate_key()
# with open("secret.key", "wb") as key_file:
#     key_file.write(key)

def load_key():
    """Load the previously generated key"""
    return open("secret.key", "rb").read()

key = load_key()
cipher_suite = Fernet(key)

def encrypt_message(message: str) -> bytes:
    return cipher_suite.encrypt(message.encode())

def decrypt_message(encrypted_message: bytes) -> str:
    return cipher_suite.decrypt(encrypted_message).decode()
