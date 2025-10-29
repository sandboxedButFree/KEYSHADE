from dotenv import load_dotenv

import os, getpass, sys

from modules.crypt import (
    generate_key,
    intialise_cipher,
    encrypt_password,
    decrypt_password,
    hash_master_password,
    encode_data,
    decode_data,
    store_environment_variables,
    generate_password_salt,
)

from modules.user import (
    load_menu,
    generate_table,
    register_user,
    user_login,
    view_credentials,
    view_single_credential,
    add_credential,
)

from storage.ascii_art import KEYSHADE, REGISTRATION_COMPLETE, LOGIN_SUCCESSFUL

try:
    load_dotenv()
except FileNotFoundError:
    print("Error! No .env file present.")

## Check if an environment variable exists for the encryption key.
if os.getenv("PASSWORD_KEY") is None:

    ## Generate Key.
    key = generate_key()

    ## base64 encoding the key for storage
    encoded_key = encode_data(key)

    # Reassigning the key to the decoded_key variable for use later.
    decoded_key = key

    ##Storing the PASSWORD_KEY as an environment variable.
    store_environment_variables(encoded_key, "PASSWORD_KEY")
else:
    encoded_key = os.getenv("PASSWORD_KEY")
    decoded_key = decode_data(encoded_key)

cipher = intialise_cipher(decoded_key)

print(KEYSHADE)

bypass = True

while bypass is True:
    print("[1] Register the Master User")
    print("[2] Login")
    print("[3] Exit Program")

    salt = generate_password_salt()

    user_input = input("Please Enter a Selection: ")

    if user_input == "1":
        username = input("Please Enter Your Master Username: ")
        password = getpass.getpass("Please Enter Your Master Password: ")
        register_user(username, password, salt, REGISTRATION_COMPLETE)

    elif user_input == "2":
        username = input("Please Enter Your Master Username: ")
        password = getpass.getpass("Please Enter Your Master Password: ")
        login = user_login(username, password, salt, LOGIN_SUCCESSFUL)
        if login is True:
            bypass = False

    elif user_input == "3":
        sys.exit()

load_menu()

while True:
    user_input = input("Please Enter a Selection: ")

    if user_input == "1":
        entries = view_credentials(cipher)
        generate_table(entries, cipher, "All Credentials")

    if user_input == "2":
        service = input("Enter The Service You Would Like To View: ")
        entry = view_single_credential(cipher, service)
        table_name = service + " Credentials"
        generate_table(entry, cipher, table_name)

    if user_input == "3":
        1 - 1

    if user_input == "4":
        website = input("Please Enter The Website You Wish To Add: ")
        username = input("Please Enter Your Username: ")
        password = getpass.getpass("Please Enter Your Password: ")
        confirmed_password = getpass.getpass("Please Confirm Your Password: ")
        if password == confirmed_password:
            add_credential(website, username, password, cipher)
        else:
            print("Passwords Don't Match, Please Try Again.")

    if user_input == "5":
        1 - 1
