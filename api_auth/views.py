from rest_framework import viewsets, permissions
from .serializers import UserSerializer, GroupSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
	lookup_field = User.USERNAME_FIELD
	lookup_url_kwarg = User.USERNAME_FIELD
	queryset = User.objects.order_by(User.USERNAME_FIELD)
	serializer_class = UserSerializer
	permission_classes = (permissions.IsAuthenticated,)


class GroupViewSet(viewsets.ModelViewSet):
	queryset = Group.objects.order_by('name')
	serializer_class = GroupSerializer
	permission_classes = (permissions.IsAdminUser,)
	