from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (DonwloadShoppingCartViewSet, FavouriteViewSet,
                    IngredientViewSet, RecipeViewSet, ShoppingCartViewSet,
                    TagViewSet)

app_name = 'recipes'

router = DefaultRouter()

router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path(
        'recipes/<str:pk>/favorite/',
        FavouriteViewSet.as_view(),
        name='favorite',
    ),
    path(
        'recipes/<str:pk>/shopping_cart/',
        ShoppingCartViewSet.as_view(),
        name='shopping_cart',
    ),
    path(
        'recipes/download_shopping_cart/',
        DonwloadShoppingCartViewSet.as_view(),
        name='download_shopping_cart',
    ),
    path('', include(router.urls)),
]
