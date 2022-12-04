from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.pagination import PageNumberPagination


def return_response(data, success, message, status, headers=None):
    try:
        if not success and message == 'Bad request!':
            data_keys = list(data.keys())
            message = "".join(data[data_keys[0]])
            message = message.replace('This', data_keys[0])
    except Exception as e:
        pass

    response_data = {"data":data, "success": success, "message": message, 'status': status}
    return Response(response_data, status=status)


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    # Now add the HTTP status code to the response.
    if response is not None and response.status_code == 404:
        response.data = {
            'data' : {"detail":"The resource was not found."},
            "status": 404,
            "success" : False,
            "message": "The resource was not found.",
        }
    return response


class CustomPagination(PageNumberPagination):

    page_size_query_param = "page_size"
    
    def get_paginated_response(self, data):
        data = {
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'limit': self.page_size,
            'data': data
        }
        return return_response(data, True, 'List Successfully Retrieved!', status.HTTP_200_OK)
