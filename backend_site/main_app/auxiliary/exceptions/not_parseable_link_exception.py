from rest_framework.exceptions import APIException

class NotParseableLinkExcepcion(APIException):
    status_code = 400
    default_detail ='Impossible to parse URL.'
    default_code = 'service_denied'

