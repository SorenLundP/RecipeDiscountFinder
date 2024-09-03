# RecipeDiscountFinder

**RecipeDiscountFinder** is a Python-based tool designed to help you find and track the best grocery offers for your recipes. By scraping online discount flyers, this tool matches ingredients from your selected recipes with ongoing promotions at various stores, helping you save money while planning your meals.

## Features
- **Ingredient Matching**: Automatically fetch discounts for ingredients listed in your recipes.
- **Store Information**: Identify which stores are offering the best prices for your ingredients.
- **Recipe Ranking**: Rank your recipes by the number of discounted ingredients to optimize your shopping.
- **Customizable Recipes**: Easily add and modify recipes to tailor the search to your needs.

### Prerequisites
You will also need to install the following Python packages:
- `requests`
- `beautifulsoup4`
Or install the requirements.txt file

### Current limitations
Currently, the tool may inadvertently match general terms, such as spices, with unrelated products (e.g., chips containing the spice). This issue arises due to the broad search criteria used during scraping.