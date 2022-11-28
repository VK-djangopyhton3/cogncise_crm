from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.customer.models import CustomerInfo
from apps.jobs.api.serializers import WorkTypeSerializer, JobSerializer
from apps.jobs.models import WorkType, Jobs
from apps.properties.models import Property
from utils.permissions import IsCommon, IsManager, IsAdmin
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

    def put(self, request):
        work_type = self.get_object(request.data["work_type_id"])
        serializer = WorkTypeSerializer(work_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(success_response(serializer.data, "Work type updated"))
        return Response(fail_response(serializer.errors, "Work type could not be updated"))

    def delete(self, request):
        work_type = self.get_object(request.data["work_type_id"])
        work_type.is_active = False
        work_type.save()
        return Response(success_response(None, "work type deleted"))


class WorkTypeSearch(ListAPIView):
    serializer_class = WorkTypeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = WorkType.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        return queryset

    message = "Company list"
    filter_backends = [SearchFilter]
    search_fields = ['id', 'work_type']


class JobsViews(APIView):
    permission_classes = [IsManager]

    def get_objects(self, jid, cid=None):
        job = Jobs.objects.filter(id=jid)
        user = self.request.user
        if user.is_staff:
            job = job.filter(agency__id=cid)
        if not CustomerInfo.objects.filter(customer=user).exists():
            job = job.filter(agent=user.userroles)
        else:
            job = job.filter(customer=user)
        return job.first()

    def put(self, request):
        job = self.get_objects(request.data['job_id'])
        if request.user.is_staff:
            job = self.get_objects(request.data['job_id'], request.data['company_id'])
        if job:
            serializer = JobSerializer(job, data={"job_status": request.data['job_status']}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(success_response(serializer.data, "Job details updated"))
            return Response(fail_response(serializer.errors, "Job could not be updated"))
        return Response(fail_response(None, "The job could not be found"))

    def post(self, request):
        data = request.data
        user = request.user

        customer = CustomerInfo.objects.get(customer__id=data['user_id'], agency=user.userroles.company)
        property_address = Property.objects.get(id=data['property_address_id'], customer=customer)
        serializer = JobSerializer(data=data)
        if serializer.is_valid():
            serializer.save(customer=customer, agent=user.userroles, property_address=property_address)
            return Response(success_response(serializer.data, 'New job created'))
        return Response(fail_response(serializer.errors, 'Job could not be created', status.HTTP_400_BAD_REQUEST))

    def get(self, request):
        job = self.get_objects(request.data['job_id'])
        if request.user.is_staff:
            job = self.get_objects(request.data['job_id'], request.data['company_id'])
        if job:
            serializer = JobSerializer(job, many=False)
            return Response(success_response(serializer.data, "Job details updated"))
        return Response(fail_response(None, "The job could not be found"))


class JobSearchList(ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Jobs.objects.all()
        if user.is_staff and not user.is_superuser:
            queryset = queryset.filter(staffassociation__user=user)
        if not user.is_staff:
            queryset = queryset.filter(agent__company=user.userroles.company)
        else:
            queryset = queryset.filter(customer__customer=user)
        return queryset

    message = "Company list"
    filter_backends = [SearchFilter, DjangoFilterBackend]
    fields = ['id', 'agent', 'agent__user__phone', 'job_status', 'created_on']
    filterset_fields = fields
    search_fields = fields
