from rest_framework.exceptions import APIException

class NotSubscribedException(APIException):
    status_code = 400
    default_detail = 'You are not subscribed to that feed. Subscribe first to read articles'
    default_code = 'service_denied'