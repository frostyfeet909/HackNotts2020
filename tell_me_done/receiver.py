# Flask webhook plus some handling of that user-input
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request
from tell_me_done import data_interface
from tell_me_done import phone_numbers
from passlib.hash import sha256_crypt

app = Flask(__name__)
ADMIN_HASH = '$5$rounds=535000$Xwnyj7m7WB.i1PVA$h3vBiuyDepNh71fH4oBWLYtrqMBmLkhYwOX7Ba5s5b5'
# Hash of super secret password


def run():
    # Run Flask consistent with ngrok
    app.run(port=3000, debug=False)


def set_admin(user, password):
    # Set user admin under certain conditions
    try:
        password = password.encode()
    except:
        print("[!] Some weird hooliganry happened with the password")
        return False

    # Verifies password against the hash (don't actually store plaintext password == more secure)
    if sha256_crypt.verify(password, ADMIN_HASH):
        print("[!] New admin: %s" % (user.name if user.name is not None else user.phone_number))
        user.admin = True
        data_interface.save_user_data(user)
        return True

    return False


def set_name(user, name):
    # Set user nickname
    user.name = name
    data_interface.save_user_data(user)


def set_newvars(user, var):
    if user.admin:
        data_interface.save_json_data(var)
        return True
    else:
        return False


@app.route("/", methods=['GET', 'POST'])
def sms():
    # Receive incoming messages
    resp = MessagingResponse()
    user = data_interface.get_user_data(request.form['From'])
    command = str(request.form['Body'])

    # Setup new user if needed
    if not user:
        user = phone_numbers.User(request.form['From'])
        data_interface.save_user_data(user)
        print("[*] New user registered: %s" % (user.name if user.name is not None else user.phone_number))
        resp.message("Welcome new user!")
        resp.message("Commands:\n admin [admin password] - Admin login \n name [name] - Set username")

    print("[*] Message from: %s" % (user.name if user.name is not None else user.phone_number))
    print("    - %s" % command)

    # Do the appropriate command
    if " " in command:
        argument = " ".join(command.split(" ")[1:])

        if command.lower().startswith("admin"):
            if set_admin(user, argument):
                resp.message("Correct password! Your an admin")
            else:
                resp.message("Wrong password! Your no admin")

        elif command.lower().startswith("name"):
            set_name(user, argument)
            resp.message("Name Set! " + "Welcome " + user.name)

        elif command.lower().startswith("newvars"):
            if set_newvars(user, argument):
                resp.message("Variables saved!")
            else:
                resp.message("You do not have permission!")

        else:
            resp.message("Command not found!")

    return str(resp)
