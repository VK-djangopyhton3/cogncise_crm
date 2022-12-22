from common.common_view_imports import *

from shared.views import CrudViewSet
from appointment.models import WorkType, Appointment, SechduleAppointment
from appointment.serializers import WorkTypeSerializer, AppointmentSerializer, SechduleAppointmentSerializer

class WorkTypeListAPIView(generics.ListAPIView):
    swagger_tag = ["appointment work types"]
    queryset = WorkType.objects.all()
    serializer_class = WorkTypeSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]


class AppointmentViewSet(CrudViewSet):
    swagger_tag = ["appointments"]
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class SechduleAppointmentViewSet(CrudViewSet):
    queryset = SechduleAppointment.objects.all()
    serializer_class = SechduleAppointmentSerializer
    # authentication_classes = [TokenAuthentication, SessionAuthentication]
    # permission_classes = [IsAuthenticated]


# class SechduleAppointmentViewSet(viewsets.ModelViewSet):
#     queryset = SechduleAppointment.objects.all()
#     serializer_class = SechduleAppointmentSerializer
#     authentication_classes = [TokenAuthentication, SessionAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get_permissions(self):
#         if self.action == 'create':
#             return [AllowAny(),]        
#         return super(AppointmentViewSet, self).get_permissions()

#     def get_queryset(self):
#         self.queryset = self.queryset.filter(user = self.request.user)
#         return self.queryset

#     def get_serializer_class(self):
#         if self.action == 'create':
#             return self.serializer_class
#         return self.serializer_class

#     def create(self, request):
#         import pdb;pdb.set_trace()
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()                  

#             # logger.info(data)
#             return return_response(serializer.data, True, 'Successfully Created!', status.HTTP_200_OK)

#         # logger.error(serializer.errors)
#         return return_response(serializer.errors, False, 'Bad request!', status.HTTP_400_BAD_REQUEST)

    
#     def list(self, request):
#         page = self.paginate_queryset(self.get_queryset())
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)

#         serializer = self.get_serializer(self.get_queryset(), many=True)

#         # logger.info(serializer.data)
#         return return_response(serializer.data, True, 'List Successfully Retrieved!', status.HTTP_200_OK)
    
#     def retrieve(self, request, pk=None):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
        
#         # logger.info(serializer.data)
#         return return_response(serializer.data, True, ' Successfully Retrieved!', status.HTTP_200_OK)

#     def update(self, request, pk=None):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data)
#         if serializer.is_valid():
#             serializer.update(instance,validated_data=serializer.validated_data)
            
#             # logger.info(serializer.data)
#             return return_response(serializer.data, True, ' Successfully Updated!', status.HTTP_200_OK)

#         # logger.error(serializer.errors)
#         return return_response(serializer.errors, False, 'Bad request!', status.HTTP_400_BAD_REQUEST)

#     def partial_update(self, request, pk=None):
#         pass

#     def destroy(self, request, pk=None):
#         instance = self.get_object()
#         self.perform_destroy(instance)

#         # logger.info('Successfully Deleted!')
#         return return_response({"detail":"object deleted"}, True, ' Successfully Deleted!', status.HTTP_200_OK)

