from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Follow, User
from .serializers import FollowUsersSerializer, FullUserSerializer


class FollowUserViewSet(UserViewSet):

    serializer_class = FullUserSerializer

    def user_subscribe(self, serializer, id=None):
        following_user = get_object_or_404(User, id=id)

        if self.request.user == following_user:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        follow = Follow.objects.get_or_create(
            user=self.request.user,
            following=following_user
        )

        return Response(FollowUsersSerializer(follow[0]).data)

    def user_unsubscribe(self, serializer, id=None):
        following_user = get_object_or_404(User, id=id)

        deleted_subscriptions = Follow.objects.filter(
            user=self.request.user,
            following=following_user
        ).delete()

        if deleted_subscriptions[0] > 0:
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(
        detail=True,
        methods=['get', 'delete'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscribe(self, serializer, id=None):
        if self.request.method == 'DELETE':
            return self.user_unsubscribe(serializer, id)
        else:
            return self.user_subscribe(serializer, id)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscriptions(self, serializer):
        follow_list = Follow.objects.filter(user=self.request.user)
        page = self.paginate_queryset(follow_list)
        serializer = FollowUsersSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
