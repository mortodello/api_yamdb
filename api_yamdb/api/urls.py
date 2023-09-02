from django.urls import include, path
from rest_framework import routers
from api.views import ReviewViewSet, CommentViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'v1/reviews', ReviewViewSet)
router_v1.register(r'v1/titles/{title_id}/reviews/{review_id}/comments/',
                   CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router_v1.urls)),
]
