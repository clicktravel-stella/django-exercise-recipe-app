from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Ingredient


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


def sample_ingredient(recipe, name='Chinese Five Spice'):
    """Create and return a sample ingredient"""

    return Ingredient.objects.create(name=name, recipe=recipe)


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
        self.assertEqual(ingredients.count(), 2)
        self.assertTrue(ingredients.filter(
            name=res.data['ingredients'][0]['name']
            ).exists())
        self.assertTrue(ingredients.filter(
            name=res.data['ingredients'][1]['name']
            ).exists())

    def test_create_recipe_invalid(self):
        """Test that recipe cannot be created without payload"""
        # Arrange
        payload = {
            'name': '',
        }
        # Act
        res = self.client.post(RECIPES_URL, payload, format='json')
        # Assert
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_full_update_recipe(self):
        """Test updating a recipe with put"""
        # Arrange
        recipe = sample_recipe()
        recipe.ingredients.add(sample_ingredient(recipe=recipe))
        payload = {
            'name': 'Korma',
            'description': 'Creamy Curry',
            'ingredients': [
                {'name': 'Chicken'},
                {'name': 'Coconut Milk'}
            ]
        }
        url = detail_url(recipe.id)
        # Act
        self.client.put(url, payload, format='json')
        recipe.refresh_from_db()
        # Assert
        self.assertEqual(recipe.name, payload['name'])
        self.assertEqual(recipe.description, payload['description'])

    def test_partial_recipe_update(self):
        """Test that recipe can be partially updated"""
        # Arrange
        recipe = sample_recipe()
        url = detail_url(recipe.id)
        payload = {'name': 'Beef bourguignon'}
        # Act
        res = self.client.patch(url, payload)
        recipe.refresh_from_db()
        # Assert
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.name, payload['name'])

    def test_delete_recipe(self):
        """Test recipe deletes successfully"""
        # Arrange
        recipe = sample_recipe()
        url = detail_url(recipe.id)
        # Act
        res = self.client.delete(url)
        # Assert
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(pk=recipe.id).exists())
