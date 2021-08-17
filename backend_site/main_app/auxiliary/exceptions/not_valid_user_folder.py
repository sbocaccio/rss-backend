from rest_framework.exceptions import APIException

class NotValidUserFolder(APIException):
    status_code = 400
    default_detail = 'This folder does not exist or is not part of any of your folders'
    default_code = 'service_denied'