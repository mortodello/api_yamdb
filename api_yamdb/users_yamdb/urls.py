from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet, MyAccount, SignUp, get_jwt_token


router_v1 = routers.SimpleRouter()
router_v1.register('v1/users', UserViewSet, 'UserYaMDB')

urlpatterns = [
    path(
        'v1/users/me/',
        MyAccount.as_view(),
        name='MyAccount',
    ),
    path('v1/auth/signup/', SignUp.as_view(), name='signup'),
    path('v1/auth/token/', get_jwt_token, name='gettoken'),
    path('', include(router_v1.urls)),
]
