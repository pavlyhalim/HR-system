from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        custom_response = {
            "success": False,
            "error": {
                "status_code": response.status_code,
                "detail": response.data,
            },
        }
        response.data = custom_response
    else:
        custom_response = {
            "success": False,
            "error": {
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "detail": "An unexpected error occurred.",
            },
        }
        response = Response(custom_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
