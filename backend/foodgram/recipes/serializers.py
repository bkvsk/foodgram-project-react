from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from users.serializers import FullUserSerializer

from .models import (FavouriteRecipe, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCartRecipe, Tag)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient.id'
    )
    amount = serializers.IntegerField()

    class Meta:
        fields = ('id', 'amount')
        model = IngredientInRecipe


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag


class RecipeTagSerializer(serializers.ModelSerializer):

    def to_representation(self, value):
        return value.id

    class Meta:
        model = Tag
        fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    author = FullUserSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = IngredientInRecipeSerializer(required=True, many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=False,
        queryset=Tag.objects.all()
    )
    is_in_favorites = serializers.SerializerMethodField(
        'check_is_in_favorites',
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        'check_is_in_shopping_cart',
    )

    def create_recipe_ingredients(self, recipe, ingredients_data):
        for ingredient in ingredients_data:
            IngredientInRecipe.objects.create(
                recipe=recipe,
                ingredient=ingredient['ingredient']['id'],
                amount=ingredient['amount'],
            )

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_recipe_ingredients(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        IngredientInRecipe.objects.filter(recipe=instance).delete()
        self.create_recipe_ingredients(instance, ingredients_data)
        instance.tags.set(tags)

        return super().update(instance, validated_data)

    def check_is_in_favorites(self, obj):
        current_user = self.context['request'].user
        if current_user.is_anonymous:
            return False

        return FavouriteRecipe.objects.filter(
            recipe=obj,
            user=current_user,
        ).exists()

    def check_is_in_shopping_cart(self, obj):
        current_user = self.context['request'].user
        if current_user.is_anonymous:
            return False

        return ShoppingCartRecipe.objects.filter(
            recipe=obj,
            user=current_user,
        ).exists()

    class Meta:
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
            'is_in_favorites',
            'is_in_shopping_cart'
        )
        model = Recipe
        read_only_fields = ('author', 'is_in_favorites', 'is_in_shopping_cart')


class RecipeFavouriteSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('recipe', 'user')
        model = FavouriteRecipe
