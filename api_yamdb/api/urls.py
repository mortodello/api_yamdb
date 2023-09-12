from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoriesViewSet, GenresViewSet, TitleViewSet,
                    ReviewViewSet, CommentViewSet, UserViewSet,
                    SignUp, get_jwt_token)

router_v1 = DefaultRouter()
router_v1.register('categories', CategoriesViewSet, basename='categories')
router_v1.register('genres', GenresViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
router_v1.register((r'titles/(?P<title_id>\d+)/reviews/'
                    r'(?P<review_id>\d+)/comments'),
                   CommentViewSet, basename='comment')
router_v1.register('users', UserViewSet, 'CustomUser')

auth_patterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('token/', get_jwt_token, name='gettoken'),
]

urlpatterns = [
    path('auth/', include(auth_patterns)),
    path('', include(router_v1.urls)),
]
