
class NotUserReceived(Exception):
    def __init__(self, message="Error: Any valid user had been passed"):
        self.message = message
        super().__init__(self.message)