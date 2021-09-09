from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingredient

# from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPES_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    """Return recipe detail URL"""
    return reverse('recipe:recipe-detail', args=[recipe_id])

def sample_recipe(**params):
    """Create and return a sample recipe"""
    defaults = {
        'name': 'A recipe name',
        'description': 'A recipe description',
    }
    defaults.update(params)

    return Recipe.objects.create(**defaults)


class RecipeApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_get_recipes(self):
        """Test getting recipes from API"""
        # Arrange
        recipe1 = sample_recipe(name='Cheese Puffs', description='puff in your cheese')
        recipe2 = sample_recipe(name='Lemon Pie', description='pie in your lemon')

        # Act
        res = self.client.get(RECIPES_URL)