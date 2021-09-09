from unittest.mock import patch

from django.test import TestCase

from core import models


class ModelTests(TestCase):

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            name='Pasta alla Stella',
            description='Pasta with super special ingredients'
        )

        self.assertEqual(str(recipe), recipe.name)
