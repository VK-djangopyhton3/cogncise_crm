from common.common_view_imports import *
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth import get_user_model, authenticate
from rest_framework.decorators import action

from core.serializers import UserSerializer, LoginSerializer, UserProfileSerializer, CheckUserSerializer, ShowUserSerializer
from core import utils

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):

    """
    User Operation View

    User can perform CRUD operation to the system.
    The data required are username, email, first_name, last_name, password, access_type.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,]


    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny(),]        
        return super(UserViewSet, self).get_permissions()

    def get_queryset(self):
        self.queryset = self.queryset.filter()
        return self.queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return self.serializer_class
        return ShowUserSerializer

    def list(self, request):
        page = self.paginate_queryset(self.get_queryset())
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(self.get_queryset(), many=True)

        # logger.info(serializer.data)
        return return_response(serializer.data, True, 'List Successfully Retrieved!', status.HTTP_200_OK)


    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                user.set_password(serializer.validated_data['password'])
                user.save()
                return return_response(serializer.data, True, 'User created Successfully!', status.HTTP_201_CREATED)

            return return_response(serializer.errors, False, 'Bad request!', status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return return_response(str(e), False, 'Bad request!', status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        # logger.info(serializer.data)
        return return_response(serializer.data, True, ' Successfully Retrieved!', status.HTTP_200_OK)

    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.update(instance,validated_data=serializer.validated_data)
            
            # logger.info(serializer.data)
            return return_response(serializer.data, True, ' Successfully Updated!', status.HTTP_200_OK)

        # logger.error(serializer.errors)
        return return_response(serializer.errors, False, 'Bad request!', status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        instance = self.get_object()
        self.perform_destroy(instance)

        # logger.info('Successfully Deleted!')
        return return_response({"detail":"object deleted"}, True, ' Successfully Deleted!', status.HTTP_200_OK)


class LoginAPIView(generics.GenericAPIView):

    """
    Login View

    User can login to the system.
    The data required are username, password.
    """
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                # if request.data['email']:
                #    user = User.objects.get(email__iexact=serializer.validated_data['email'].lower())
                # else:
                user = User.objects.get(username__iexact=serializer.validated_data['username'].lower() )
            except ObjectDoesNotExist:
                return return_response('User does not exist, please register now!', False, 'User does not exist, please register now!', status.HTTP_404_NOT_FOUND, )

            password = serializer.validated_data['password']
            user = authenticate(username=user.username, password=password)

            if user is not None and user.is_active:
                if user.is_authenticated:
                    utils.login_user(request, user)
                    serializer = ShowUserSerializer(user)
                    return return_response(serializer.data, True, "User logged in successfully", status.HTTP_200_OK, ) 

            return return_response('Unable to log in with provided credentials.', False, 'Incorrect Username or Password, Please contact with support or try to login again!', status.HTTP_400_BAD_REQUEST)

        # logger.debug(f"{message},'user':{request.user}, 'status':{serializer.errors}")
        return return_response(serializer.errors, False, 'Bad request!', status.HTTP_400_BAD_REQUEST)



class LogoutAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            utils.logout_user(request)
            return return_response(
                None, True, 'Logout successfully!', status.HTTP_200_OK
            )
        except Exception as e:
            return return_response(
                None, False, 'Unauthorized user!', status.HTTP_401_UNAUTHORIZED
            )



class RetrieveUserExistsAPIView(generics.GenericAPIView):
    serializer_class = CheckUserSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            if 'email' in request.data.keys():
                user = User.objects.get(
                    email__iexact=serializer.validated_data['email'].lower()
                )
                if user is not None:
                    return return_response(
                        '', True, 'Email already exist!', status.HTTP_200_OK
                    )
                else:
                    return return_response(
                        '', True, 'Email DoesNotExist!', status.HTTP_200_OK
                    )
            elif 'username' in request.data.keys():
                user = User.objects.get(
                    username__iexact=serializer.validated_data['username'].lower()
                )
                if user is not None:
                    return return_response(
                        '', True, 'Username already exist!', status.HTTP_200_OK
                    )

                else:
                    return return_response(
                        '', True, 'Username DoesNotExist!', status.HTTP_200_OK
                    )
            else:
                return return_response(
                    '',
                    False,
                    'Unable to log in with provided credentials.',
                    status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return return_response(
                serializer.errors,
                False,
                'Unable to log in with provided credentials.',
                status.HTTP_400_BAD_REQUEST,
            )


class RetrieveUpdateProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    """Used to retrieve user data before updation"""

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return return_response(
            serializer.data,
            True,
            'User profile successfully retrieved!',
            status.HTTP_200_OK,
        )

    """Used for updation of user data"""

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.update(instance, validated_data=serializer.validated_data)
            serializer = self.get_serializer(instance)
            return return_response(
                serializer.data,
                True,
                'User profile successfully updated!',
                status.HTTP_200_OK,
            )
        return return_response(
            serializer.errors, False, 'Bad request!', status.HTTP_400_BAD_REQUEST
        )

