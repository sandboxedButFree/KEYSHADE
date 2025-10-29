import base64, os

from cryptography.fernet import Fernet
from hashlib import sha256


def generate_key():
    return Fernet.generate_key()


def intialise_cipher(key):
    return Fernet(key)


def encrypt_password(cipher, password):
    return cipher.encrypt(password.encode()).decode()


def decrypt_password(cipher, encrypted_password):
    return cipher.decrypt(encrypted_password.encode()).decode()


def encode_data(data):
    return base64.b64encode(data).decode("utf-8")


def decode_data(encoded_data):
    return base64.b64decode(encoded_data).decode("utf-8")


def store_environment_variables(key, environment_variable, filename=".env"):
    print(key)
    stored_value = environment_variable + " = " + key + "\n"
    with open(filename, "a") as f:
        f.write(stored_value)


def hash_master_password(password, salt):
    decoded_salt = base64.b64decode(salt)
    encoded_password = password.encode("utf-8")
    return sha256(encoded_password + decoded_salt).hexdigest()


def generate_password_salt():
    if os.getenv("PASSWORD_SALT") is None:
        salt = os.urandom(32)
        encoded_salt = encode_data(salt)
        store_environment_variables(encoded_salt, "PASSWORD_SALT")
    else:
        return os.getenv("PASSWORD_SALT")
