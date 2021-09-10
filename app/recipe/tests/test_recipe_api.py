from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

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
        """Test getting recipes"""
        # Arrange
        recipe1 = sample_recipe(name='Cheese Puffs',
                                description='puff in your cheese')
        recipe2 = sample_recipe(name='Lemon Pie',
                                description='pie in your lemon')

        # Act
        res = self.client.get(RECIPES_URL)

        # Assert
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data[0].get('name'), recipe1.name)
        self.assertEqual(res.data[1].get('name'), recipe2.name)
        self.assertEqual(res.data[0].get('description'), recipe1.description)
        self.assertEqual(res.data[1].get('description'), recipe2.description)

    def test_get_single_recipe(self):
        """Test getting one recipe"""
        # Arrange
        recipe = sample_recipe()
        url = detail_url(recipe.id)

        # Act
        res = self.client.get(url)

        # Assert
        self.assertEqual(res.data.get('name'), recipe.name)

    def test_create_recipe(self):
        """Test creating a recipe"""
        # Arrange
        payload = {
            'name': 'Chocolate Fondont',
            'description': 'Melt worthy',
            'ingredients': [
                {'name': 'Chocolate'},
                {'name': 'Other stuff'}
            ]
        }
        # Act
        res = self.client.post(RECIPES_URL, payload, format='json')

        # Assert
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        ingredients = recipe.ingredients.all()
        print(ingredients[0])
        self.assertEqual(ingredients.count(), 2)
        self.assertTrue(ingredients.filter(
            name=res.data['ingredients'][0]['name']
            ).exists())
        self.assertTrue(ingredients.filter(
            name=res.data['ingredients'][1]['name']
            ).exists())
