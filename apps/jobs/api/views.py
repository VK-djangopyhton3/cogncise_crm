from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.company.models import Companies
from apps.customer.models import CustomerInfo
from apps.jobs.api.serializers import WorkTypeSerializer, JobSerializer, JobTransferHistorySerializer
from apps.jobs.models import WorkType, Jobs, JobTransferHistory
from apps.properties.models import Property
from apps.users.api.serializers import UserSerializer
from apps.users.models import StaffAssociate
from utils.permissions import IsStaff, IsManager, IsAdmin
from utils.responseformat import fail_response, success_response

User = get_user_model()


# Create your views here.
@api_view(['POST'])
@permission_classes([IsStaff])
def create_work_type(request):
    serializer = WorkTypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(success_response(serializer.data, 'New work type created'))
    return Response(fail_response(serializer.errors, 'Work type could not be created', status.HTTP_400_BAD_REQUEST))


@api_view(['PUT'])
@permission_classes([IsStaff])
def update_work_type(request):
    work_type = WorkType.objects.get(id=request.data['id'])
    serializer = WorkTypeSerializer(work_type, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(success_response(serializer.data, 'Update success full'))
    return Response(fail_response(serializer.errors, 'There were issues in the request', status.HTTP_400_BAD_REQUEST))


class WorkTypeSearchList(ListAPIView):
    serializer_class = WorkTypeSerializer
    permission_classes = [IsManager]

    def get_queryset(self):
        queryset = WorkType.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        return queryset

    message = "work type list"
    filter_backends = [SearchFilter]
    search_fields = ['work_type']


@api_view(["DELETE"])
@permission_classes([IsStaff])
def delete_work_type(request):
    work_type = WorkType.objects.get(id=request.data['id'])
    work_type.is_active = False
    work_type.save()
    return Response(success_response(None, "Work type deleted"))


'''
Create Lead
'''


def job_assign(company_id, job_id):
    job = Jobs.objects.get(id=job_id)
    jt = JobTransferHistory.objects.filter(job__id=job_id)
    jt.update(is_current_assignee=False)
    agency = Companies.objects.get(id=company_id)
    job_owner = JobTransferHistory.objects.create(job=job, agency=agency, transfer_count=jt.count())
    serializer = JobTransferHistorySerializer(job_owner)
    return serializer.data


@api_view(['POST'])
@permission_classes([IsManager])
def add_job(request):
    work_type = WorkType.objects.get(id=request.data['work_type_id'])
    customer = CustomerInfo.objects.get(id=request.data['customer_user_id'])
    property_address = Property.objects.get(id=request.data['property_address_id'], customer=customer)
    agent = request.user
    if Jobs.objects.filter(property_address=property_address, customer=customer, work_type=work_type).exists():
        return Response(fail_response(None, "This job already exists", status.HTTP_208_ALREADY_REPORTED))
    serializer = JobSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(work_type=work_type, customer=customer, agent=agent, property_address=property_address)
        jt = job_assign(request.user.userroles.company.id, serializer.data['id'])
        data = serializer.data
        data['agency_transfer_history'] = jt
        return Response(success_response(data, 'New job created'))
    return Response(fail_response(serializer.errors, 'Job could not be created', status.HTTP_400_BAD_REQUEST))


@api_view(['PUT'])
@permission_classes([IsManager])
def update_job_status(request):
    job = Jobs.objects.get(id=request.data['job_id'])
    serializer = JobSerializer(job, data={'job_status': request.data['job_status']})
    if serializer.is_valid():
        serializer.save()
        return Response(success_response(serializer.data, "Job status updated"))
    return Response(fail_response(serializer.errors, 'job status could not be update'))


@api_view(['PUT'])
@permission_classes([IsAdmin])
def transfer_job_agency(request):
    job = request.data['job_id']
    company = request.data['company_id']
    jt = job_assign(company, job)
    return Response(success_response(jt, "Job status updated"))


@api_view(['PUT'])
@permission_classes([IsManager])
def transfer_job_agent(request):
    job = Jobs.objects.get(id=request.data['job_id'])
    agent = User.objects.get(id=request.data['agent_user_id'], userroles__company=request.user.userroles.company)
    serializer = JobSerializer(job, data={'agent': agent}, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(success_response(serializer.data, "agent changed to " + agent.name))
    return Response(fail_response(serializer.errors, "agent could not be changed", status.HTTP_400_BAD_REQUEST))


class JobListSearch(ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsManager]

    def get_queryset(self):
        queryset = Jobs.objects.filter()
        if self.request.user.is_staff and not self.request.user.is_superuser:
            queryset.filter(jobtransferhistory=self.request.GET['company_id'])
        if not self.request.user.is_staff:
            queryset.filter(jobtransferhistory__agency=self.request.user.userroles.company)
        return queryset

    message = "Job list"
    filter_backends = [SearchFilter]
    search_fields = ["id", "customer__customer__name", "property_address__postcode", "property_address__property_type",
                     "property_address__building_name", "agent", "job_status"]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_job_details(request):
    job = Jobs.objects.filter(id=request.GET['job_id'])
    if not request.user.is_superuser:
        job = job.filter(jobtransferhistory__agency__staffassociate__user__id=request.user.id)
    if not request.user.is_staff:
        agency = request.user.userroles.company
        job = job.filter(jobtransferhistory__agency=agency, jobtransferhistory__is_current_assignee=True)
    if job.exists():
        serializer = JobSerializer(job.first(), many=False)
        return Response(success_response(serializer.data, "job " + str(job[0].id) + " details"))
    return Response(fail_response(None, "Job with this ID does not exists", status.HTTP_401_UNAUTHORIZED))
