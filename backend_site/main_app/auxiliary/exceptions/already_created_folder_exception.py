from rest_framework.exceptions import APIException

class AlreadyCreatedFolder(APIException):
    status_code = 400
    default_detail = 'This folder is already created. You cannot create it twice.'
    default_code = 'service_denied'