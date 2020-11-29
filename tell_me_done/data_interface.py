# Reading/Saving user data, twilio info and anything else
from os.path import join, dirname, realpath
from json import load as json_load
from json import dump as json_dump
from pickle import dumps, loads  # Written in Python 3.9, json probably faster but wanted to try pickle + shelve
import shelve  # Shelve is lovely


def get_json_data():
    # Get data from json file
    path = dirname(realpath(__file__))
    with open(join(path, "resources", "keys.json"), "r") as file:
        data = json_load(file)

    return data


def save_json_data(key, content):
    # Save data to json file
    path = dirname(realpath(__file__))
    data = {key: content}
    with open(join(path, "resources", "vars.json"), "a") as file:
        json_dump(data, file)


def get_user_data(phone_number=None):
    # Get user data from shelve DB
    users = set()
    path = join(dirname(realpath(__file__)), "resources", "users")
    with shelve.open(path) as db:
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
    path = join(dirname(realpath(__file__)), "resources", "users")
    with shelve.open(path) as db:
        db[user.phone_number] = dumps(user)
