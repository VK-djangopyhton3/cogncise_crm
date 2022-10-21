from django.contrib.auth import get_user_model
from django.views.generic import UpdateView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.api.serializers import UserSerializer
from utils.permissions import IsAdmin
from utils.responseformat import success_response, fail_response

User = get_user_model()


# Create your views here.
class UserCreateView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(success_response(serializer.data, 'New user added'))
        return Response(fail_response(serializer.errors, 'New user could not be added'))


