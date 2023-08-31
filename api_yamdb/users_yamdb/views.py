from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework import mixins
from django.shortcuts import get_object_or_404

from .models import YaMDBUser
from .permissions import Administrator
from .serializers import UserSerializer

# viewset for admin rest api
class UserViewSet(viewsets.ModelViewSet):

    serializer_class = UserSerializer

    permission_classes = [Administrator]
    pagination_class = LimitOffsetPagination

    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def get_queryset(self, username=None):
        if username is not None:
            user = YaMDBUser.objects.get(username=username)
            queryset = YaMDBUser.filter(author=user)
            return queryset
        else:
            queryset = YaMDBUser.objects.all()
            return queryset
        
        
    lookup_field = 'username'
    lookup_value_regex = '[a-zA-Z0-9$&(._)\-]+'


# viewset for simple rest api
class UpdateDeleteViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
    viewsets.GenericViewSet):
    pass


class MyAccount(UpdateDeleteViewSet):

    serializer_class = UserSerializer

    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
