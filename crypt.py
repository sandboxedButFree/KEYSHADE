from cryptography.fernet import Fernet
import hashlib

def generate_key():
    return Fernet.generate_key()

def intialise_cipher(key):
    return Fernet(key)

def encrypt_password(cipher, password):
    return cipher.encrypt(password.encode()).decode()

def decrypt_password(cipher, encrypted_password):
    return cipher.decrypt(encrypt_password.encode()).decode()
