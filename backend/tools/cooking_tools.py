import pandas as pd
from typing import List, Dict, Any
import re

class CookingTools:
    def __init__(self):
        """Initialize cooking tools with recipe data"""
        try:
            self.recipes_df = pd.read_csv('data/recipes.csv')
        except Exception as e:
            print(f"Error loading recipes file: {str(e)}")
            self.recipes_df = pd.DataFrame()
        
    def recipe_finder(self, query: str) -> str:
        """Find recipes based on ingredients, cuisine, or difficulty"""
        if self.recipes_df.empty:
            return "Xin lỗi, không thể tải dữ liệu công thức nấu ăn."
            
        # Convert query to lowercase for case-insensitive search
        query = query.lower()
        
        # Search in multiple columns
        matches = self.recipes_df[
            self.recipes_df['recipe_name'].str.lower().str.contains(query) |
            self.recipes_df['cuisine'].str.lower().str.contains(query) |
            self.recipes_df['ingredients'].str.lower().str.contains(query)
        ]
        
        if matches.empty:
            return "Không tìm thấy công thức phù hợp với yêu cầu của bạn."
            
        # Format the first matching recipe
        recipe = matches.iloc[0]
        ingredients = recipe['ingredients'].replace(';', ', ')
        instructions = recipe['instructions'].replace(';', '\n')
        
        return (
            f"Tìm thấy công thức: {recipe['recipe_name']}" + "\n" +
            f"Phong cách: {recipe['cuisine']}" + "\n" +
            f"Độ khó: {recipe['difficulty']}" + "\n" +
            f"Thời gian: {recipe['prep_time'] + recipe['cook_time']} phút" + "\n" +
            f"Nguyên liệu: {ingredients}" + "\n" +
            "Hướng dẫn:" + "\n" +
            f"{instructions}" + "\n" +
            f"Mẹo: {recipe['tips']}"
        )

    def ingredient_substitute(self, ingredient: str) -> str:
        """Suggest substitutes for common ingredients"""
        # Common substitutions dictionary
        substitutes = {
            "butter": "margarine, olive oil, coconut oil",
            "eggs": "mashed banana, applesauce (in baking), tofu (in savory dishes)",
            "milk": "almond milk, soy milk, oat milk",
            "cream": "coconut cream, cashew cream",
            "flour": "almond flour, coconut flour, oat flour",
            "sugar": "honey, maple syrup, stevia",
            "soy sauce": "coconut aminos, tamari",
            "rice": "quinoa, cauliflower rice",
            "pasta": "zucchini noodles, spaghetti squash",
            "meat": "tofu, tempeh, mushrooms",
        }
        
        ingredient = ingredient.lower()
        if ingredient in substitutes:
            return f"For {ingredient}, you can use: {substitutes[ingredient]}"
        return f"No common substitutes found for {ingredient}. Try asking for a specific dietary requirement."

    def portion_calculator(self, recipe_name: str, desired_servings: int) -> str:
        """Calculate ingredient portions for desired number of servings"""
        # Find the recipe
        recipe = self.recipes_df[self.recipes_df['recipe_name'].str.lower() == recipe_name.lower()]
        if recipe.empty:
            return "Recipe not found."
            
        # Get original servings and ingredients
        original_servings = recipe.iloc[0]['servings']
        ingredients = recipe.iloc[0]['ingredients'].split(';')
        
        # Calculate multiplier
        multiplier = desired_servings / original_servings
        
        # Adjust quantities
        adjusted_ingredients = []
        for ingredient in ingredients:
            # Try to find and adjust numeric quantities
            match = re.search(r'(\d+\.?\d*)', ingredient)
            if match:
                original_qty = float(match.group(1))
                new_qty = original_qty * multiplier
                adjusted = ingredient.replace(match.group(1), str(round(new_qty, 1)))
                adjusted_ingredients.append(adjusted)
            else:
                adjusted_ingredients.append(ingredient)
        
        ingredients_text = ', '.join(adjusted_ingredients)
        return (
            f"Adjusted recipe for {desired_servings} servings" + "\n" +
            "Ingredients:" + "\n" +
            f"{ingredients_text}"
        )

    def cooking_timer(self, recipe_name: str) -> str:
        """Get timing information for a recipe"""
        recipe = self.recipes_df[self.recipes_df['recipe_name'].str.lower() == recipe_name.lower()]
        if recipe.empty:
            return "Recipe not found."
            
        r = recipe.iloc[0]
        instructions = r['instructions'].replace(';', '\n')
        
        return (
            f"Timing for {r['recipe_name']}:" + "\n" +
            f"Prep Time: {r['prep_time']} minutes" + "\n" +
            f"Cooking Time: {r['cook_time']} minutes" + "\n" +
            f"Total Time: {r['prep_time'] + r['cook_time']} minutes" + "\n\n" +
            "Instructions with timing:" + "\n" +
            f"{instructions}"
        )

    def nutrition_info(self, recipe_name: str) -> str:
        """Get nutritional information for a recipe"""
        recipe = self.recipes_df[self.recipes_df['recipe_name'].str.lower() == recipe_name.lower()]
        if recipe.empty:
            return "Recipe not found."
            
        r = recipe.iloc[0]
        nutrition = dict(item.split(':') for item in r['nutrition'].split(';'))
        
        return (
            f"Nutritional Information for {r['recipe_name']} (per serving)" + "\n" +
            f"Calories: {nutrition['calories']}" + "\n" +
            f"Protein: {nutrition['protein']}" + "\n" +
            f"Carbohydrates: {nutrition['carbs']}" + "\n\n" +
            f"Recipe serves: {r['servings']} people"
        )

    def list_ingredients(self, recipe_name: str) -> str:
        """Liệt kê nguyên liệu cần thiết cho một món ăn"""
        if self.recipes_df.empty:
            return "Xin lỗi, không thể tải dữ liệu công thức nấu ăn."
            
        try:
            # Tìm món ăn trong database
            recipe = self.recipes_df[self.recipes_df['recipe_name'].str.contains(recipe_name, case=False, na=False)]
            
            if recipe.empty:
                return f"Xin lỗi, tôi không tìm thấy thông tin về món {recipe_name} trong cơ sở dữ liệu."
            
            # Lấy thông tin nguyên liệu
            ingredients = recipe.iloc[0]['ingredients']
            return f"Để làm món {recipe_name}, bạn cần những nguyên liệu sau:\n{ingredients}"
            
        except Exception as e:
            return f"Có lỗi khi tìm nguyên liệu: {str(e)}" 