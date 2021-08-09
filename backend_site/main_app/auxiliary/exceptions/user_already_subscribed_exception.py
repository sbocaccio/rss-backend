from rest_framework.exceptions import APIException


class UserAlreadySubscribedException(APIException):
    status_code = 409
    default_detail = 'User is already subscribed to that page.'
    default_code = 'service_denied'