from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters, status
from rest_framework import mixins
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
import math
import random

from .models import YaMDBUser
from .permissions import Administrator
from .serializers import (
    UserSerializer,
    UserEmailSerializer,
)

from api_yamdb import settings


# viewset for admin rest api
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [Administrator]
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def get_queryset(self, username=None):
        if username:
            return get_object_or_404(YaMDBUser, username=username)

        return YaMDBUser.objects.all()

    lookup_field = 'username'
    lookup_value_regex = r'[a-zA-Z0-9$&(._)\-]+'


# viewset for simple rest api
class UpdateDeleteViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                          viewsets.GenericViewSet):
    pass


class MyAccount(UpdateDeleteViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# viewset for get confirmation code
class SignUp(GenericAPIView):
    serializer_class = UserEmailSerializer
    permission_classes = [AllowAny, ]

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
        data = request.data
        username = data['username']
        user_email = data['email']
        data['confirmation_code'] = self.generate_confirmation_code()

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        subject = 'welcome to Ya_mdb project!'
        message = (
            f'Dear {username}, thank you for registering in yambd api service.'
            f'It is your confirmation code: {data["confirmation_code"]}'
        )

        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user_email, ]
        send_mail(subject, message, email_from,
                  recipient_list, fail_silently=False,)

        return Response(serializer.data, status=status.HTTP_200_OK)


# viewset for get token
@api_view(['POST'])
def get_jwt_token(request):
    data = request.data
    user = get_object_or_404(YaMDBUser, username=data['username'])

    if user.confirmation_code == data['confirmation_code']:
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        return Response({'token': token}, status=status.HTTP_200_OK)

    resp = {'confirmation_code': 'Неверный код подтверждения'}
    return Response(resp, status=status.HTTP_400_BAD_REQUEST)


# class GetToken(GenericAPIView):

#     serializer_class = TokenSerializer

#     permission_classes = [AllowAny,]

#     def post(self, request):
#         data=request.data
#         user = get_object_or_404(
#             YaMDBUser,
#             username=data['username']
#         )

#         if user.confirmation_code!=data['confirmation_code']:
#             resp = {'confirmation_code': 'Invalid confirmation_code'}
#             return Response(resp, status=status.HTTP_400_BAD_REQUEST)
#         refresh = RefreshToken.for_user(user)
#         data['tokens'] = str(refresh.access_token)
#         serializer = self.serializer_class(data=data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'token': data['tokens']}, status=status.HTTP_200_OK)
