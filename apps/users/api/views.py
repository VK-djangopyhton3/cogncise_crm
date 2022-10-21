from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.api.serializers import UserSerializer
from utils.permissions import IsAdmin
from utils.responseformat import success_response, fail_response

User = get_user_model()


# Create your views here.
class UserViews(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        pass

    def post(self, request):

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(success_response(serializer.data,'New user added'))

        return Response(fail_response(serializer.errors,'New user could not be added'))

    def put(self, request):
        pass

    def delete(self, request):
        pass

    def get_queryset(self, request):
        qs = User.objects.all()
        if not request.user.is_staff:
            qs = User.objects.filter(userrole__company__company_name=request.user.company.name)
        return qs
