from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='название ингредиента',
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='единицы измерения',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='название тега',
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name='цвет тега',
    )
    slug = models.SlugField(
        max_length=30,
        unique=True,
        verbose_name='слаг тега',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='автор рецепта',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='название рецепта',
    )
    image = models.ImageField(
        upload_to='recipe_images/',
        verbose_name='фото блюда',
    )
    text = models.TextField(
        verbose_name='описание рецепта',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='теги рецепта',
    )
    cooking_time = models.IntegerField(
        validators=[
            MinValueValidator(1, message='the value must be a natural number'),
        ],
        default=1,
        verbose_name='время приготовления',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), ],
        default=1,
        verbose_name='количество ингредиента',
    )

    def __str__(self):
        return f'{self.ingredient} in {self.recipe}'

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['ingredient', 'recipe'],
            name='unique_ingredient_in_recipe',
        )]
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'


class FavouriteRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='рецепт',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='пользователь',
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_recipe_in_favorites',
        )]
        verbose_name = 'Рецепт в избранном'
        verbose_name_plural = 'Рецепты в избранном'


class ShoppingCartRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='рецепт',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='пользователь',
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_recipe_in_shopping_cart',
        )]
        verbose_name = 'Рецепт в корзине'
        verbose_name_plural = 'Рецепты в корзине'
