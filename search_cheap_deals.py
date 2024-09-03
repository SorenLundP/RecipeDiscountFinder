recipes = {
    "Chilli_sin_carne": [
        "Kidneybønner", "hvidløg", "soltørrede tomater", "løg", 
        "squash", "gulerødder", "mørk chokolade", "creme fraiche", 
        "nachos", "ris"
    ],
    "Honning_glaseret_kylling": [],
    "Tortillas_med_bønnefyld": [
        "Tortillas", "kidneybønner", "sorte bønner", "salsa", "majs", 
        "salat", "agurk", "tomat", "creme fraiche", "Taco krydderi"
    ],
    "Dahl": [
        "Røde linser", "ingefær", "creme fraiche", "ris", "naanbrød", 
        "hvidløg", "karry", "hakkede tomater"
    ],
    "Pita_med_tunsalat": [
        "Pita brød", "agurk", "tomat", "salat", "gulerod", 
        "tun", "hytteost", "creme fraiche", "citron", "mayonnaise"
    ],
    "Pizza": [
        "Mel", "pizza bund", "tomatsovs", "revet ost", "ost", 
        "skinke strimler", "pepperoni", "champignon"
    ],
    "Pølsehorn": [
        "Pizzadej", "pølser"
    ],
    "Lasagne": [
        "Lasagneplader", "ost", "parmesan", "oksekød", "løg", 
        "mælk", "smør", "hvidløg"
    ],
    "Vegetarlasagne": [
        "Lasagneplader", "ost", "parmesan", "løg", "mælk", 
        "smør", "hvidløg", "squash", "aubergine", "selleri", "gulerødder"
    ],
    "Biksemad": [],
    "Brændende_kærlighed": [
        "Kartofler", "mælk", "smør", "løg", "bacon", "rødbeder"
    ],
    "Risotto": [
        "Risottoris", "champignon", "radiser", "rejer", "hvidvin"
    ],
    "Pasta_med_fløde_og_spinat": [
        "svampe", "hvidløg"
    ],
    "One_pot_pasta_med_chorizo": [],
    "Mexicansk_salat": [
        "ris", "sorte bønner", "avo", "majs", "rødløg", "kylling"
    ],
    "Nudelret_med_grøntsager_og_æg": [
        "broccoli"
    ],
    "Æggekage_med_broccoli": [
        "Tærtedej", "smør", "æg", "broccoli", "bacon", "creme fraiche"
    ]
}


import requests
from bs4 import BeautifulSoup

# Base URL for searching
base_url = "https://etilbudsavis.dk/soeg/{keyword}?business_ids=11deC%2CDWZE1w%2C9ba51"

# Dictionary to store offers for each ingredient
offers = {}

# Function to fetch and store offers for an ingredient
def fetch_and_store_offers(ingredient):
    search_url = base_url.format(keyword=ingredient)
    response = requests.get(search_url)
    if response.status_code != 200:
        print(f"Failed to fetch offers for {ingredient}")
        return

    # Parse HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all offer elements
    offer_elements = soup.find_all('a', class_='OfferList__OfferListItemLink-sc-bj82vg-3 gIYFqK')
    
    offers_for_ingredient = []
    for offer_element in offer_elements:
        # Extracting the name of the item
        item_name_element = offer_element.find('header', {'itemprop': 'name'})
        item_name = item_name_element.text.strip() if item_name_element else 'No name found'

        # Extracting the price of the item
        offer_price_element = offer_element.find('span', {'class': 'OfferList___StyledSpan2-sc-bj82vg-14 euySqQ'})
        offer_price = offer_price_element.text.replace('\xa0', ' ') if offer_price_element else 'No price found'

        # Extracting the store of the item
        offer_store_element = offer_element.find('div', {'class': 'OfferList___StyledDiv5-sc-bj82vg-16 hTCTZf'})
        offer_store = offer_store_element.text.strip() if offer_store_element else 'Unknown'

        # Append the offer details to the list
        offers_for_ingredient.append({
            'name': item_name,
            'price': offer_price,
            'store': offer_store
        })

    if offers_for_ingredient:  # Only store if there are offers
        if ingredient in offers:
            offers[ingredient].extend(offers_for_ingredient)
        else:
            offers[ingredient] = offers_for_ingredient

# Loop through each recipe and its ingredients
for recipe, ingredients in recipes.items():
    print(f"Checking offers for {recipe}")

    # Fetch offers for each ingredient
    for ingredient in ingredients:
        fetch_and_store_offers(ingredient)

    # Print the offers for the current recipe
    print(f"Offers for {recipe}:")
    for ingredient in ingredients:
        if ingredient in offers:
            print(f"  Ingredient: {ingredient}")
            for discount in offers[ingredient]:
                print(f"    Name: {discount['name']}, Store: {discount['store']}, Price: {discount['price']}")
        else:
            print(f"  Ingredient: {ingredient} - No offers found")
    print()

# Rank recipes by the number of items on discount
recipe_ranking = {recipe: len([ing for ing in ingredients if ing in offers]) for recipe, ingredients in recipes.items()}
sorted_recipes = sorted(recipe_ranking.items(), key=lambda x: x[1], reverse=True)

print("Recipes ranked by most items on discount:")
for recipe, count in sorted_recipes:
    print(f"{recipe}: {count} items on discount")
