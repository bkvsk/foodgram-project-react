from django.contrib import admin

from .models import (FavouriteRecipe, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCartRecipe, Tag)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author',)
    list_filter = ('name', 'author', 'tags',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)
    ordering = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)
    list_filter = ('name',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientInRecipe)
admin.site.register(Tag, TagAdmin)
admin.site.register(ShoppingCartRecipe)
admin.site.register(FavouriteRecipe)
