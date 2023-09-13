from django.db.models import Avg
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, mixins, status
from rest_framework.decorators import api_view, action
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .permissions import (IsAdmin,
                          IsAdminOrReadOnly,
                          IsAuthorAdminModeratorOrReadOnly)
from .serializers import (
    CategoriesSerializer,
    GenresSerializer,
    TitleGetSerializer,
    TitlePostSerializer,
    ReviewSerializer,
    CommentSerializer,
    UserSerializer
)
from api_yamdb import settings
from reviews.models import Categories, Genres, Title, Review
from users_yamdb.models import CustomUser


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
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(BaseCategoriesGenresViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    serializer_class = TitleGetSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]
    # перечисление методов необходимо для исключения метода PUT
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action == 'create':
            return TitlePostSerializer
        if self.action == 'partial_update':
            return TitlePostSerializer
        return TitleGetSerializer


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
    """Вью функция для получения токена."""
    data = request.data
    username = data.get('username')
    if not username:
        resp = {'username': 'Поле username необходимо!'}
        return Response(resp, status=status.HTTP_400_BAD_REQUEST)

    confirmation_code = data.get('confirmation_code')
    if not confirmation_code:
        resp = {'confirmation_code': 'Поле confirmation_code необходимо!'}
        return Response(resp, status=status.HTTP_400_BAD_REQUEST)

    user = get_object_or_404(CustomUser, username=username)

    if default_token_generator.check_token(user, confirmation_code):
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        return Response({'token': token}, status=status.HTTP_200_OK)

    resp = {'confirmation_code': 'Неверный confirmation_code!'}
    return Response(resp, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    # перечисление методов необходимо для исключения метода PUT
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [IsAdmin]
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    lookup_value_regex = r'[a-zA-Z0-9$&(._)\-]+'

    @action(
        methods=['patch', 'get'],
        permission_classes=[IsAuthenticated],
        detail=False
    )
    def me(self, request, *args, **kwargs):
        """Action-функция для получения
           и частичного изменения данных профиля."""
        user = self.request.user
        serializer = self.get_serializer(user)
        if self.request.method == 'PATCH':
            # здесь неправильно пояснил в прошлый раз
            # этот if проверяет было ли добавлено поле role
            # в информацию для изменения данных юзера
            # и если да, то игнорирует его
            if request.data.get('role'):
                request.data._mutable = True
                del request.data['role']
                request.data._mutable = False

            serializer = self.get_serializer(user,
                                             data=request.data,
                                             partial=True)
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
            # здесь выбирается первый объект из queryset созданного выше
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
        subject = 'Добро пожаловать на проект yamdb!'
        message = (
            f'Дорогой {user.username}, спасибо'
            f'за регистрацию на yambd api service.'
            f'Это ваш confirmation code: {token}'
        )
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail(subject, message, email_from,
                  recipient_list, fail_silently=False,)
        return Response(request.data, status=status.HTTP_200_OK)
