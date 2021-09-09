from rest_framework import serializers

from core.models import Recipe

"""
class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('name',)
"""

class RecipeSerializer(serializers.ModelSerializer):
    """Serialize a recipe"""
    ingredients = 'butter'

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'description', 
        )
        read_only_fields = ('id',)
