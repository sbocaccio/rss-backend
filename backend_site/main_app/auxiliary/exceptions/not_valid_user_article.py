
from rest_framework.exceptions import APIException

class NotValidUserArticle(APIException):
    status_code = 400
    default_detail = 'This article does not exist or is not part of any of your subscriptions'
    default_code = 'service_denied'