from django.urls import include, path
from rest_framework import routers

from .views import (
    TokenObtainView,
    UserRegistrationView,
    UserViewSet,
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet,
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews',
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments',
)

urlpatterns = [
    path(
        'api/v1/auth/signup/',
        UserRegistrationView.as_view(),
        name='signup',
    ),
    path(
        'api/v1/auth/token/',
        TokenObtainView.as_view(),
        name='get_token',
    ),
    path('api/v1/', include(router.urls)),
]
