from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet, MyAccount

router_v1 = routers.SimpleRouter()
router_v1.register('v1/users', UserViewSet, 'UserYaMDB')



urlpatterns = [
    path(
        'v1/users/me/',
        MyAccount.as_view({
            'get': 'retrieve',
            'patch': 'update'
        }),
        name='MyAccount',
    ),
    path('', include(router_v1.urls)),
]
