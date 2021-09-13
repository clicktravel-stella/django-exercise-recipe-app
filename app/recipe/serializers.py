from rest_framework import serializers

from core.models import Recipe, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """Serialize an ingredient"""
    class Meta:
        model = Ingredient
        fields = ('name',)
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serialize a recipe"""
    ingredients = IngredientSerializer(
        many=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'description', 'ingredients',
        )
        read_only_fields = ('id',)

    def create(self, validated_data):
        """Create recipe"""
        ingredient_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)

        if ingredient_data:
            for ingredient in ingredient_data:
                Ingredient.objects.create(**ingredient, recipe=recipe)

        return recipe

    def update(self, instance, validated_data):
        """Update Recipe"""
        ingredient_data = validated_data.pop('ingredients', None)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description
            )
        instance.save()

        Ingredient.objects.filter(recipe_id=self.instance.id).delete()

        recipe = Recipe.objects.get(id=self.instance.id)

        if ingredient_data:
            for ingredient in ingredient_data:
                Ingredient.objects.create(**ingredient, recipe=recipe)

        return instance
