class NotRegisteredUsersException(Exception):
    def __init__(self, message="Error: Any of the users passed is registered. Try again passing registered user"):
        self.message = message
        super().__init__(self.message)