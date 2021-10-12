from recipes.models import Recipe
from rest_framework import serializers


class RecipeCountFollowUserField(serializers.Field):
    def get_attribute(self, instance):
        return Recipe.objects.filter(author=instance.following)

    def to_representation(self, recipe_list):
        return recipe_list.count()


class RecipeFollowUserField(serializers.Field):
    def get_attribute(self, instance):
        return Recipe.objects.filter(author=instance.following)

    def to_representation(self, recipe_list):
        recipe_data = []
        for recipe in recipe_list:
            recipe_data.append(
                {
                    "id": recipe.id,
                    "name": recipe.name,
                    "image": recipe.image.url,
                    "cooking_time": recipe.cooking_time,
                }
            )
        return recipe_data
