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
        """Find recipes based on exact name match"""
        if self.recipes_df.empty:
            return "Xin lỗi, không thể tải dữ liệu công thức nấu ăn."
            
        # Convert query to lowercase for case-insensitive search
        query = query.lower()
        
        # Search for exact matches in recipe_name
        matches = self.recipes_df[
            self.recipes_df['recipe_name'].str.lower() == query
        ]
        
        if matches.empty:
            return f"Xin lỗi, tôi không tìm thấy món {query} trong cơ sở dữ liệu của mình. Tôi chỉ có thể cung cấp thông tin về các món có trong danh sách."
            
        # Format the matching recipe
        recipe = matches.iloc[0]
        ingredients = recipe['ingredients'].replace(';', '\n- ')
        instructions = recipe['instructions'].replace(';', '\n')
        
        return (
            f"Đây là công thức nấu món {recipe['recipe_name']}:\n\n" +
            f"Phong cách: {recipe['cuisine']}\n" +
            f"Độ khó: {recipe['difficulty']}\n" +
            f"Thời gian chuẩn bị: {recipe['prep_time']} phút\n" +
            f"Thời gian nấu: {recipe['cook_time']} phút\n" +
            f"Phục vụ: {recipe['servings']} người\n\n" +
            f"Nguyên liệu cần có:\n- {ingredients}\n\n" +
            "Các bước thực hiện:\n" +
            f"{instructions}\n\n" +
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
            return f"Xin lỗi, tôi không tìm thấy món {recipe_name} trong cơ sở dữ liệu của mình."
            
        r = recipe.iloc[0]
        instructions = r['instructions'].replace(';', '\n')
        
        return (
            f"Thông tin thời gian nấu món {r['recipe_name']}:\n\n" +
            f"Thời gian chuẩn bị: {r['prep_time']} phút\n" +
            f"Thời gian nấu: {r['cook_time']} phút\n" +
            f"Tổng thời gian: {r['prep_time'] + r['cook_time']} phút\n\n" +
            "Các bước thực hiện:\n" +
            f"{instructions}"
        )

    def nutrition_info(self, recipe_name: str) -> str:
        """Get nutritional information for a recipe"""
        recipe = self.recipes_df[self.recipes_df['recipe_name'].str.lower() == recipe_name.lower()]
        if recipe.empty:
            return f"Xin lỗi, tôi không tìm thấy món {recipe_name} trong cơ sở dữ liệu của mình."
            
        r = recipe.iloc[0]
        nutrition = dict(item.split(':') for item in r['nutrition'].split(';'))
        
        return (
            f"Thông tin dinh dưỡng cho món {r['recipe_name']} (cho mỗi phần ăn):\n\n" +
            f"Calories: {nutrition['calories']}\n" +
            f"Protein: {nutrition['protein']}\n" +
            f"Carbohydrates: {nutrition['carbs']}\n" +
            f"Chất béo: {nutrition['fat']}\n\n" +
            f"Món ăn này đủ cho {r['servings']} người ăn."
        )

    def list_ingredients(self, recipe_name: str) -> str:
        """Liệt kê nguyên liệu cần thiết cho một món ăn"""
        if self.recipes_df.empty:
            return "Xin lỗi, không thể tải dữ liệu công thức nấu ăn."
            
        # Tìm món ăn trong database bằng tên chính xác
        recipe = self.recipes_df[self.recipes_df['recipe_name'].str.lower() == recipe_name.lower()]
        
        if recipe.empty:
            return f"Xin lỗi, tôi không tìm thấy món {recipe_name} trong cơ sở dữ liệu của mình."
        
        # Lấy và định dạng thông tin nguyên liệu
        ingredients = recipe.iloc[0]['ingredients'].replace(';', '\n- ')
        return f"Để nấu món {recipe_name}, bạn cần những nguyên liệu sau:\n- {ingredients}" 