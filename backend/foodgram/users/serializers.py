from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework import serializers

from .fields import RecipeCountFollowUserField, RecipeFollowUserField
from .models import Follow, User


class FullUserSerializer(DjoserUserSerializer):
    is_subscribed = serializers.SerializerMethodField(
        'check_is_subscribed',
        read_only=True
    )

    def check_is_subscribed(self, obj):
        if self.context['request'].user.is_anonymous:
            return False

        if self.context['request'].user == obj:
            return True

        if Follow.objects.filter(
            following=self.context['request'].user,
            user=obj
        ):
            return True
        return False

    class Meta:
        model = User
        fields = list(DjoserUserSerializer.Meta.fields) + ['is_subscribed']
        read_only_fields = (
            list(DjoserUserSerializer.Meta.read_only_fields) +
            ['is_subscribed']
        )


class FollowUsersSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='following.email')
    id = serializers.ReadOnlyField(source='following.id')
    username = serializers.ReadOnlyField(source='following.username')
    first_name = serializers.ReadOnlyField(source='following.first_name')
    last_name = serializers.ReadOnlyField(source='following.last_name')
    is_subscribed = serializers.ReadOnlyField(default=True)
    recipes = RecipeFollowUserField()
    recipes_count = RecipeCountFollowUserField()

    class Meta:
        read_only_fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
        model = Follow
