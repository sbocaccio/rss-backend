
class NotUserReceived(Exception):
    def __init__(self, message="Error: Any registered user had been passed. Try again passing registered users."):
        self.message = message
        super().__init__(self.message)