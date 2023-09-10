from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet, SignUp, get_jwt_token

router_v1 = routers.SimpleRouter()
router_v1.register('v1/users', UserViewSet, 'CustomUser')

auth_patterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('token/', get_jwt_token, name='gettoken'),
]

urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
    path('', include(router_v1.urls)),
]
