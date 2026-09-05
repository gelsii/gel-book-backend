from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

load_dotenv()

main_enc = Fernet(key='UeRCZ1RU5_xlBKPi0W-gq5a2y-ZTkL23IvUZxEBD5z8=')

def encrypt_private_word(text: str):
    encrypted_text = main_enc.encrypt(text.encode())

    return encrypted_text.decode()

def decrypt_text(text: str):
    decrypted_text = main_enc.decrypt(token=text)
    
    return decrypted_text.decode()