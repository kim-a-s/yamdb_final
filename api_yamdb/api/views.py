from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from rest_framework import filters, views, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.pagination import PageNumberPagination

from .filters import TitleFilter
from reviews.models import Category, Genre, Title, Review
from .permissions import (IsAdmin,
                          IsAdminOrReadOnly,
                          IsAuthorAdminModerateOrReadOnly,)
from .serializers import (SelfUserSerializer, TokenObtainSerializer,
                          UserRegistrationSerializer, UserSerializer,
                          CategorySerializer, GenreSerializer,
                          TitleReadSerializer, TitlePostSerializer,
                          ReviewSerializer, CommentSerializer,)


User = get_user_model()


def send_confirmation_code(user):
    token = default_token_generator.make_token(user)
    send_mail(
        'Подтверждение регистрации на yamdb',
        f'Ваш код подтверждения: {token}',
        "admin@yamdb.com",
        [user.email],
    )


class UserRegistrationView(views.APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user, created = User.objects.get_or_create(**serializer.data)
            except IntegrityError:
                if User.objects.filter(
                    email=serializer.data['email'],
                ).exists():
                    raise ValidationError(
                        'Пользователь с таким email уже существует'
                    )
                raise ValidationError(
                    'Пользователь с таким username уже существует'
                )
            send_confirmation_code(user)
            return Response(serializer.data)


class TokenObtainView(views.APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = TokenObtainSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(
                User, username=serializer.data['username'])
            if default_token_generator.check_token(
                user,
                serializer.data['confirmation_code'],
            ):
                access_token = AccessToken.for_user(user)
                data = {'token': str(access_token)}
                return Response(data)
            raise ValidationError('Invalid username and/or confirmation_code')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin, ]
    filter_backends = (
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    search_fields = ('username',)
    lookup_field = 'username'
    ordering = ('date_joined',)
    http_method_names = ['get', 'post', 'patch', 'delete', ]

    @action(
        detail=False,
        url_path='me',
        methods=['get'],
        permission_classes=[IsAuthenticated, ]
    )
    def get_self_user_info(self, request):
        serializer = SelfUserSerializer(request.user)
        return Response(serializer.data)

    @get_self_user_info.mapping.patch
    def patch_self_user_info(self, request):
        serializer = SelfUserSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    search_fields = ('name', )
    lookup_field = 'slug'
    ordering = ('id', )


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    search_fields = ('name', )
    lookup_field = 'slug'
    ordering = ('id', )


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score'))
    serializer_class = TitlePostSerializer
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = PageNumberPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    ordering = ('id',)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitlePostSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorAdminModerateOrReadOnly,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('pub_date',)
    ordering = ('pub_date',)

    def get_permissions(self):
        if self.action == 'create':
            return (IsAuthenticated(),)
        return super().get_permissions()

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title,)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorAdminModerateOrReadOnly,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('pub_date',)
    ordering = ('pub_date',)

    def get_permissions(self):
        if self.action == 'create':
            return (IsAuthenticated(),)
        return super().get_permissions()

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id,)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id,)
        serializer.save(author=self.request.user, review=review,)
