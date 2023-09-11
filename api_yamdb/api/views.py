from rest_framework import viewsets, filters, mixins, status
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, action
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator

from api_yamdb import settings
from .permissions import (IsAdmin,
                          IsAdminOrReadOnly,
                          IsAuthorAdminModeratorOrReadOnly)
from reviews.models import Categories, Genres, Title, Review
from users_yamdb.models import CustomUser
from .serializers import (
    CategoriesSerializer,
    GenresSerializer,
    TitleSerializer,
    ReviewSerializer,
    CommentSerializer,
    UserSerializer
)


class BaseCategoriesGenresViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'


class BaseCommentReviewViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthorAdminModeratorOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']


class CategoriesViewSet(BaseCategoriesGenresViewSet):
    serializer_class = CategoriesSerializer

    def get_queryset(self, slug=None):
        if slug:
            return get_object_or_404(Categories, slug=slug)
        return Categories.objects.all()


class GenresViewSet(BaseCategoriesGenresViewSet):
    serializer_class = GenresSerializer

    def get_queryset(self, slug=None):
        if slug:
            return get_object_or_404(Genres, slug=slug)
        return Genres.objects.all()


class TitleViewSet(viewsets.ModelViewSet):
    """За различие в отображении данных на POST и GET запрос
       отвечает метод to_representation в сериализаторе"""
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year')
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        """Метод поддерживает фильтрацию по категории/жанру"""
        queryset = Title.objects.all()
        rating: int
        category = self.request.query_params.get('category')
        genre = self.request.query_params.get('genre')
        if category is not None:
            queryset = queryset.filter(category__slug=category)
        if genre is not None:
            queryset = queryset.filter(genre__slug=genre)
        return queryset


class CommentViewSet(BaseCommentReviewViewSet):
    serializer_class = CommentSerializer

    def get_review(self):
        return get_object_or_404(
            Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(review=self.get_review(), author=self.request.user)


class ReviewViewSet(BaseCommentReviewViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        title=get_object_or_404(Title,
                                                id=self.kwargs['title_id']))


@api_view(['POST', ])
def get_jwt_token(request):
    """View function for get token."""
    data = request.data
    username = data.get('username')
    if not username:
        resp = {'username': 'Field username required'}
        return Response(resp, status=status.HTTP_400_BAD_REQUEST)

    confirmation_code = data.get('confirmation_code')
    if not confirmation_code:
        resp = {'confirmation_code': 'Field confirmation_code required'}
        return Response(resp, status=status.HTTP_400_BAD_REQUEST)

    user = get_object_or_404(CustomUser, username=username)

    if default_token_generator.check_token(user, confirmation_code):
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        return Response({'token': token}, status=status.HTTP_200_OK)

    resp = {'confirmation_code': 'Invalid confirmation_code'}
    return Response(resp, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsAdmin]
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    lookup_value_regex = r'[a-zA-Z0-9$&(._)\-]+'

    def get_queryset(self, username=None):
        if username:
            return get_object_or_404(CustomUser, username=username)

        return CustomUser.objects.all()

    @action(
        methods=['patch', 'get'],
        permission_classes=[IsAuthenticated],
        detail=False,
        url_path='me',
        url_name='me'
    )
    def me(self, request, *args, **kwargs):
        """Action function for get and patch profile data."""
        user = self.request.user
        serializer = self.get_serializer(user)
        if self.request.method == 'PATCH':
            # protect against unauthorized role changes
            if request.data.get('role'):
                request.data._mutable = True
                del request.data['role']
                request.data._mutable = False

            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)


class SignUp(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny, ]

    def post(self, request):
        users = CustomUser.objects.filter(
            username=request.data.get('username')
        )
        if users.exists():
            user = users[0]
            serializer = self.serializer_class(instance=user,
                                               data=request.data, partial=True)
        else:
            serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        user, _ = CustomUser.objects.get_or_create(
            username=request.data.get('username'),
            email=request.data.get('email')
        )
        token = default_token_generator.make_token(user,)
        subject = 'welcome to Ya_mdb project!'
        message = (
            f'Dear {user.username}, thank you'
            f'for registering in yambd api service.'
            f'It is your confirmation code: {token}'
        )
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail(subject, message, email_from,
                  recipient_list, fail_silently=False,)
        return Response(request.data, status=status.HTTP_200_OK)
