from django.db import models


class Recipe(models.Model):
    """Recipe object"""
    name = models.TextField(blank=False)
    description = models.TextField()

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient Object"""
    name = models.TextField()
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients',
        null=True,
    )

    def __str__(self):
        return self.name
