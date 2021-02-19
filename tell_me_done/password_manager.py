# Save and check hashed password using sha256
from passlib.hash import sha256_crypt
from tell_me_done import data_interface


def encrypt_password(password):
    # Hash the password using sha256
    password = password.encode()
    password = sha256_crypt.hash(password)

    return password


def verify_password(password):
    # Verify the password against the one stored
    try:
        password = password.encode()
    except:
        print("[!!] Some weird hooliganry happened with the password")
        raise SystemExit

    admin_password = data_interface.get_json_data()["ADMIN_PASSWORD"]

    if sha256_crypt.verify(password, admin_password):
        return True

    return False
