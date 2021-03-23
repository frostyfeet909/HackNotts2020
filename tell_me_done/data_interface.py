# Reading/Saving user data, twilio info and anything else
from os.path import join, dirname, realpath, isfile, isdir
from os import remove, mkdir
from json import load as json_load
from json import dump as json_dump
# Written in Python 3.9, json probably faster but wanted to try pickle + shelve
from pickle import dumps, loads
from time import sleep
from getpass import getpass
from tell_me_done import password_manager
import shelve  # Shelve is lovely


def request_keys(account_SID=True, auth_token=True, phone_number=True, password=True):
    # Request and Store twilio keys
    print("[!] Twilio account details required!")
    print("\n")

    if account_SID:
        print("Twilio account SID:")
        account_SID = input(">> ")

    if auth_token:
        print("Twilio authentication token:")
        auth_token = getpass(prompt='>> ')

    if phone_number:
        print("Twili phone number:")
        phone_number = input(">> ")

    if password:
        print("Password for admins:")
        password = getpass(prompt='>> ')

        if password == "":
            password = "password"

    password = password_manager.Password(password)
    save_json_data(account_SID, auth_token, phone_number, password.hash)


def check_dir(path):
    # Check there's a resources folder, run on user visible functions and those run from Notifier
    if not isdir(join(path, "resources")):
        mkdir(join(path, "resources"))


def get_json_data():
    # Get data from json file
    path = dirname(realpath(__file__))
    check_dir(path)

    if not isfile(join(path, "resources", "keys.json")):
        request_keys()

    with open(join(path, "resources", "keys.json"), "r") as file:
        data = json_load(file)

    if any(item == "" for item in data.values()):
        request_keys()

    return data


def save_json_data(account_SID, auth_token, phone_number, password):
    # Save data to json file
    path = dirname(realpath(__file__))

    data = {"TWILIO_ACCOUNT_SID": account_SID,
            "TWILIO_AUTH_TOKEN": auth_token, "TWILIO_PHONE_NUMBER": phone_number, "ADMIN_PASSWORD": password}

    with open(join(path, "resources", "keys.json"), "a") as file:
        json_dump(data, file)


def save_json_vars(var):
    # Save data to json file
    path = dirname(realpath(__file__))
    data = {"ADMIN_VAR": var}

    with open(join(path, "resources", "vars.json"), "a") as file:
        json_dump(data, file)


def get_vars(wait=True):
    # Get variables stored by admin
    path = dirname(realpath(__file__))
    check_dir(path)
    file_loc = join(path, "resources", "vars.json")

    while True:
        if isfile(file_loc):
            with open(file_loc, "r") as file:
                data = json_load(file)

            remove(file_loc)
            return data["ADMIN_VAR"]

        elif not wait:
            return None

        sleep(1)


def get_user_data(phone_number=None):
    # Get user data from shelve DB
    users = set()
    path = dirname(realpath(__file__))
    check_dir(path)

    with shelve.open(join(path, "resources", "users")) as db:
        for key in list(db.keys()):
            if phone_number is None:
                users.add(loads(db[key]))
            elif phone_number == key:
                return loads(db[key])

    if len(users) == 0:
        users = None

    return users


def save_user_data(user):
    # Save user data to shelve DB (to be persistent data must be explicitly re-stored after every change)
    path = dirname(realpath(__file__))
    check_dir(path)

    with shelve.open(join(path, "resources", "users")) as db:
        db[user.phone_number] = dumps(user)
