import json, os
from rich.console import Console
from rich.table import Table
from modules.crypt import hash_master_password, encrypt_password, decrypt_password
from storage.constants import USER_JSON, PASSWORD_JSON, COLUMNS


def load_menu():
    print("[1] View All Stored Services")
    print("[2] View Credentials for a Websites")
    print("[3] View All Credentials")
    print("[4] Add a New Credential")
    print("[5] Exit Program")

def generate_table(entries, cipher, table_name):
    table = Table(title=table_name)
    rows = []
    for i in entries:
        temp_list = []
        temp_list.append(i["service"])
        temp_list.append(i["entry"]["username"])
        decrypted_password = decrypt_password(cipher, i["entry"]["password"])
        temp_list.append(decrypted_password)
        rows.append(temp_list)
        temp_list = []

    columns = COLUMNS

    for column in columns:
        table.add_column(column, style="white")

    for row in rows:
        table.add_row(*row, style="bright_green")

    console = Console()
    console.print(table)


def register_user(username, password, salt, art, filename=USER_JSON):
    master_password = hash_master_password(password, salt)
    registered_user = {"username": username, "password": master_password}

    try:
        with open(filename, "x") as f:
            json.dump(registered_user, f)
    except FileExistsError:
        with open(filename, "w") as f:
            json.dump(registered_user, f)

    print(art)


def user_login(username, password, salt, art, filename=USER_JSON):
    try:
        with open(filename, "r") as file:
            user_details = json.load(file)
    except FileNotFoundError:
        print("Error You Have Not Registered A Master User")

    print(user_details)
    master_password = hash_master_password(password, salt)
    if (
        user_details["username"] == username
        and user_details["password"] == master_password
    ):
        print(art)
        return True
    else:
        print("Error! Incorrect Login Details")
        return False


def view_credentials(cipher, filename=PASSWORD_JSON):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            entries = json.load(file)

    return entries

def view_single_credential(cipher, service, filename=PASSWORD_JSON):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            entries = json.load(file)
            print(entries)

    for entry in entries:
        if entry['service'].lower() is service.lower:
            return entry
        
    print("Service Not Found")


def add_credential(website, username, password, cipher, filename=PASSWORD_JSON):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                entries = json.load(file)
        except json.JSONDecodeError:
            entries = []

    encrypted_password = encrypt_password(cipher, password)

    credential_entry = {
        "service": website,
        "entry": {"username": username, "password": encrypted_password},
    }
    entries.append(credential_entry)

    with open(filename, "w") as f:
        json.dump(entries, f)
