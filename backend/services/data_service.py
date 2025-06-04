import pandas as pd
import os
from typing import Dict, Any, List, Sequence

class DataService:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        self.recipes_df = pd.read_csv(os.path.join(self.data_dir, 'recipes.csv'))
        
    def get_recipe(self, name: str) -> Dict[str, Any]:
        """Get recipe by name"""
        recipe = self.recipes_df[self.recipes_df['name'].str.lower() == name.lower()]
        if not recipe.empty:
            return recipe.iloc[0].to_dict()
        return {}

    def search_recipes(self, query: str, by: str = 'ingredients') -> Sequence[Dict[str, Any]]:
        """Search recipes by ingredients or cuisine"""
        if by == 'ingredients':
            matches = self.recipes_df[self.recipes_df['ingredients'].str.contains(query, case=False, na=False)]
        elif by == 'cuisine':
            matches = self.recipes_df[self.recipes_df['cuisine'].str.contains(query, case=False, na=False)]
        else:
            return []
        
        return matches.to_dict('records')

    def get_nutrition_info(self, recipe_name: str) -> Dict[str, Any]:
        """Get nutritional information for a recipe"""
        recipe = self.get_recipe(recipe_name)
        return recipe.get('nutrition', {})

    def get_cooking_time(self, recipe_name: str) -> Dict[str, int]:
        """Get prep and cook time for a recipe"""
        recipe = self.get_recipe(recipe_name)
        return {
            'prep_time': recipe.get('prep_time', 0),
            'cook_time': recipe.get('cook_time', 0)
        } 