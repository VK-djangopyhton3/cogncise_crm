import requests
from django.contrib.auth import get_user_model
from django.http import Http404
from django.views.generic import UpdateView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.api.serializers import UserSerializer
from utils.permissions import IsAdmin, IsUser
from utils.responseformat import success_response, fail_response

User = get_user_model()


# Create your views here.
class UserCreateOrDeleteView(APIView):
    permission_classes = [IsAdmin | IsUser]

    def get_object(self, request):
        return User.objects.get(id=request.data.user_id)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(success_response(serializer.data, 'New user added'))
        return Response(fail_response(serializer.errors, 'New user could not be added'))



api_view(['DELETE'])
@permission_classes[IsAdmin]
def delete(request):
    pass