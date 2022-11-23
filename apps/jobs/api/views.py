from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.jobs.api.serializers import WorkTypeSerializer
from apps.jobs.models import WorkType
from utils.permissions import IsCommon
from utils.responseformat import success_response, fail_response


# Create your views here.

class WorkTypeView(APIView):
    permission_classes = [IsCommon]

    def get_object(self, pk):
        return WorkType.objects.get(id=pk)

    def post(self, request):
        serializer = WorkTypeSerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(success_response(serializer.data, "Work type created"))
        return Response(fail_response(serializer.errors, "New work type could not be added"))

    def put(self):
        work_type = self.get_object(self.request.data["work_type_id"])
        serializer = WorkTypeSerializer(work_type)
        if serializer.save():
            serializer.save()
            return Response(success_response(serializer.data, "Work type updated"))
        return Response(fail_response(serializer.errors, "Work type could not be updated"))

    def delete(self):
        work_type = self.get_object(self.request.data["work_type_id"])
        work_type.is_active = False
        work_type.save()
        return Response(success_response())
