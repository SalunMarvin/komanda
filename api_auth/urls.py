from rest_framework.routers import DefaultRouter
from .views import UserViewSet, GroupViewSet

user_router = DefaultRouter()
user_router.register(r'users', UserViewSet)
user_router.register(r'groups', GroupViewSet)