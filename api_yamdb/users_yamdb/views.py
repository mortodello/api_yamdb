import math
import random

from rest_framework import viewsets
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters, status
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

from .models import CustomUser
from api.permissions import (
    IsAdmin,
)
from .serializers import UserSerializer
from api_yamdb import settings


# viewset for get token
@api_view(['POST', ])
def get_jwt_token(request):
    data = request.data
    username = data.get('username')
    if not username:
        resp = {'username': 'Field username required'}
        return Response(resp, status=status.HTTP_400_BAD_REQUEST)

    confirmation_code = data.get('confirmation_code')
    if not confirmation_code:
        resp = {'confirmation_code': 'Field confirmation_code required'}
        return Response(resp, status=status.HTTP_400_BAD_REQUEST)

    user = get_object_or_404(CustomUser, username=username)

    if user.confirmation_code == confirmation_code:
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        return Response({'token': token}, status=status.HTTP_200_OK)

    resp = {'confirmation_code': 'Invalid confirmation_code'}
    return Response(resp, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsAdmin]
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    lookup_value_regex = r'[a-zA-Z0-9$&(._)\-]+'

    def get_queryset(self, username=None):
        if username:
            return get_object_or_404(CustomUser, username=username)

        return CustomUser.objects.all()


class MyAccount(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'patch']

    def get_object(self):
        return self.request.user

    def patch(self, request):
        # protect against unauthorized role changes
        if request.data.get('role'):
            request.data._mutable = True
            del request.data['role']
            request.data._mutable = False
        user = self.get_object()
        serializer = self.serializer_class(instance=user,
                                           data=request.data, partial=True)
        # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(request.data, status=status.HTTP_400_BAD_REQUEST)


# viewset for get confirmation code
class SignUp(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny,]

    # function to generate confirmation code
    def generate_confirmation_code(self):
        # Declare a string variable which stores all chars
        string = ('0123456789abcdefghijklmnopqrstuvwxyz'
                  'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        code = ""
        length = len(string)
        for i in range(6):
            code += string[math.floor(random.random() * length)]
        return code

    def post(self, request):
        users = CustomUser.objects.filter(username=request.data.get('username'))
        if users.count() > 0:
            user = users[0]
            serializer = self.serializer_class(instance=user,
                                               data=request.data, partial=True)
        else:
            serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = serializer.instance

        user.confirmation_code = self.generate_confirmation_code()
        user.save(force_update=True)
        subject = 'welcome to Ya_mdb project!'
        message = (
            f'Dear {user.username}, thank you'
            f'for registering in yambd api service.'
            f'It is your confirmation code: {user.confirmation_code}'
        )
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail(subject, message, email_from,
                  recipient_list, fail_silently=False,)
        return Response(request.data, status=status.HTTP_200_OK)
