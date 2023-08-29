from django.urls import include, path
from rest_framework import routers
from api.views import ReviewViewSet

router = routers.DefaultRouter()
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
