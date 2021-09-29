from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
    )
    color = models.CharField(
        max_length=7,
        unique=True,
    )
    slug = models.SlugField(
        max_length=30,
        unique=True,
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
    )
    mesurement_unit = models.CharField(
        max_length=200,
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    name = models.CharField(
        max_length=200,
    )
    image = models.ImageField(
        upload_to='recipes/',
    )
    text = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='ingredients',
        through='IngredientInRecipe',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tags',
    )
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1), ],
        default=1,
    )

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), ],
        default=1,
    )

    def __str__(self):
        return f'{self.ingredient} in {self.recipe}'
