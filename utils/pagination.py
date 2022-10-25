from rest_framework import pagination, status
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data, message=None):
        return Response({
            'response_code': status.HTTP_200_OK,
            'success': True,
            'message': message,
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,

            'data': data
        })
