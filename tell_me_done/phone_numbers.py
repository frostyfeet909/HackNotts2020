class User:
    def __init__(self, number):
        # Template for user information
        self.phone_number = number  # Assumed one unique for each user
        self.admin = False
        self.name = None
        self.notifications = True
