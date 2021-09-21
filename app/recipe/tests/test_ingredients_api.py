from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')


class IngredientsAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_ingredient_list(self):
        """Test retrieving a list of ingredients"""
        # Arrange
        Ingredient.objects.create(name='Sugar')
        Ingredient.objects.create(name='Salt')
        # Act
        res = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        # Assert
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_ingredient_successful(self):
        """Test creating a new ingredient"""
        # Arrange
        payload = {'name': 'Chilli'}
        # Act
        self.client.post(INGREDIENTS_URL, payload)
        # Assert
        exists = Ingredient.objects.filter(
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """Test creating invalid ingredient fails"""
        # Arrange
        payload = {'name': ''}
        # Act
        res = self.client.post(INGREDIENTS_URL, payload)
        # Assert
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
