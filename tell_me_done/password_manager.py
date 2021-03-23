# Save and check hashed password using sha256
from passlib.hash import sha256_crypt
from tell_me_done import data_interface


class Password:
    def __init__(self, password):
        self.hash = self._encrypt(password)

    def _encrypt(self, password):
        # Hash the password using sha256
        try:
            password = password.encode()
        except:
            print("[!!] Some weird hooliganry happened with the password")
            raise SystemExit

        password = sha256_crypt.hash(password)

        return password

    def verify_admin(self):
        # Verify the password against the one stored
        admin_password = data_interface.get_json_data()["ADMIN_PASSWORD"]

        return sha256_crypt.verify(password, admin_password)
