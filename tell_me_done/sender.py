# Defines notifier class and deals with all sending messages
from twilio.rest import Client
from tell_me_done import data_interface


class Notifier:
    # Main class that sends messages
    def __init__(self, receive=True, done_message="Simulation finished!", var_message="Program requires some variables!"):
        data_json = data_interface.get_json_data()
        self.twilio_number = data_json['TWILIO_PHONE_NUMBER']
        self.done_message = done_message  # Message for when sim is done
        self.var_message = var_message  # Message for what vars admins need to give
        self.client = Client(
            data_json['TWILIO_ACCOUNT_SID'], data_json['TWILIO_AUTH_TOKEN'])

        if receive:
            # Need a separate process to watch for incoming messages
            from tell_me_done import receiver
            from multiprocessing import Process
            self.receiver = Process(target=receiver.run)
            self.receiver.start()
        else:
            self.receiver = None

    def shutdown(self):
        # Shutdown the Flask server properlyish
        if self.receiver is not None:
            print("[*] Flask shutdown")
            self.receiver.terminate()
            self.receiver.join()

    def notify(self, message=None, admin_only=False, done=False, need_vars=False):
        # Broadcast (notfiy) some message to all users
        if message is not None:
            pass
        elif done:
            message = self.done_message
        elif need_vars:
            message = self.var_message
        else:
            print("[!] A message is required")
            return False

        users = data_interface.get_user_data()

        if users is None:
            print("[!] No users matched")
            return False

        for user in users:
            if (not admin_only or (admin_only and user.admin)) and user.notifications:
                print("<< Message sent to %s" %
                      (user.name if user.name is not None else user.phone_number))
                self.send(message, None, user=user)

        return True

    def send(self, message, phone_number, user=None):
        # Send a specific message to some phone number
        if user is None:
            user = data_interface.get_user_data(phone_number)

        if user is None:
            print("[!] No users match this number")
            return False
        else:
            print("<< Message sent to %s" %
                  (user.name if user.name is not None else user.phone_number))
            if user.name is not None:
                message = user.name + " " + message

            self.client.messages.create(body=message,
                                        from_=self.twilio_number,
                                        to=user.phone_number
                                        )

        return True
