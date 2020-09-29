from django.http import JsonResponse


class ServiceException(Exception):
    http_code = 500

    def __init__(self, message):
        if not isinstance(message, dict):
            raise Exception('ValidationError message should be dictionary')
        self.message = message

    def get_response(self):
        return JsonResponse(
            data={
                'message': self.message,
            },
            status=self.http_code
        )


class ValidationError(ServiceException):
    http_code = 400


class ConflictError(ServiceException):
    http_code = 409
