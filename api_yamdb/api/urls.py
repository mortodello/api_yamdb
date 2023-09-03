from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet, ReviewViewSet, CommentViewSet

router_v1 = DefaultRouter()
router_v1.register('v1/categories', CategoriesViewSet, basename='categories')
router_v1.register('v1/genres', GenresViewSet, basename='genres')
router_v1.register('v1/titles', TitlesViewSet, basename='titles')
router_v1.register(r'v1/titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
router_v1.register(r'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/',
                   CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router_v1.urls)),
]
