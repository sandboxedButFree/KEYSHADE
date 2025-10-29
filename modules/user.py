import json, os, sys
from rich.console import Console
from rich.table import Table
from modules.crypt import hash_master_password, encrypt_password, decrypt_password
from storage.constants import USER_JSON, PASSWORD_JSON, COLUMNS


def load_menu():
    print("[1] View All Stored Services")
    print("[2] View Credentials for a Website")
    print("[3] View All Credentials")
    print("[4] Add a New Credential")
    print("[5] Update a Credential")
    print("[6] Delete a Credential")
    print("[7] Exit Program")


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


def view_services(filename=PASSWORD_JSON):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            entries = json.load(file)
    else:
        print("password.json doesn't exist")
        return 0

    table_name = "Websites"
    table = Table(title=table_name)
    rows = []
    columns = ["Website"]

    for entry in entries:
        website = entry["service"]
        temp_list = []
        temp_list.append(website)
        rows.append(temp_list)

    for column in columns:
        table.add_column(column, style="white")

    for row in rows:
        table.add_row(*row, style="bright_green")

    console = Console()
    console.print(table)

    return 0


def view_credentials(cipher, filename=PASSWORD_JSON):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            entries = json.load(file)
    else:
        print("password.json doesn't exist")
        return 0

    table = Table(title="Passwords")
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

    return 0


def view_single_credential(cipher, service, filename=PASSWORD_JSON):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            entries = json.load(file)
    else:
        print("password.json doesn't exist")
        return 0

    table_name = service + " Password"
    table = Table(title=table_name)
    rows = []

    for entry in entries:
        website = entry["service"]
        if website.lower() == service.lower():
            temp_list = []
            temp_list.append(website)
            temp_list.append(entry["entry"]["username"])
            decrypted_password = decrypt_password(cipher, entry["entry"]["password"])
            temp_list.append(decrypted_password)
            rows.append(temp_list)

            columns = COLUMNS

            for column in columns:
                table.add_column(column, style="white")

            for row in rows:
                table.add_row(*row, style="bright_green")

            console = Console()
            console.print(table)
            return 0

    print("Service Not Found!")


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


def update_credential(service, username, password, cipher, filename=PASSWORD_JSON):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                entries = json.load(file)
        except json.JSONDecodeError:
            print("Error Reading Passwords File, JSON Malformed or Non-existent.")

    encrypted_password = encrypt_password(cipher, password)

    for entry in entries:
        website = entry["service"]
        if website.lower() == service.lower():
            entry["entry"]["username"] = username
            entry["entry"]["password"] = encrypted_password
            print("Credential Updated")

    with open(filename, "w") as f:
        json.dump(entries, f)


def delete_credential(service, filename=PASSWORD_JSON):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                entries = json.load(file)
        except json.JSONDecodeError:
            print("Error Reading Passwords File, JSON Malformed or Non-existent.")

    for entry in entries:
        website = entry["service"]
        if website.lower() == service.lower():
            entries.remove(entry)

    with open(filename, "w") as f:
        json.dump(entries, f)


def exiting_program(art):
    print(art)

    sys.exit()
