from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet

router_v1 = DefaultRouter()
router_v1.register('v1/categories', CategoriesViewSet, basename='categories')
router_v1.register('v1/genres', GenresViewSet, basename='genres')
router_v1.register('v1/titles', TitlesViewSet, basename='titles')

urlpatterns = [
    path('', include(router_v1.urls)),

]
