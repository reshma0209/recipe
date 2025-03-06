from flask import Flask, render_template, request
import requests
import time
import json

app = Flask(__name__)

def get_recipes(query_params=None):
    url = "https://the-mexican-food-db.p.rapidapi.com/"
    headers = {
        'x-rapidapi-key': "44ea5782b6mshfc5d9605f874bf9p1d40cdjsn001f5a24f788",
        'x-rapidapi-host': "the-mexican-food-db.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=query_params)
    if response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", 1))
        time.sleep(retry_after)
        response = requests.get(url, headers=headers, params=query_params)
    response.raise_for_status()
    return response.json()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/find_recipes', methods=['GET'])
def find_recipes():
    query_params = {
        'ingredients': request.args.get('ingredients', ''),
        'min_calories': request.args.get('min_calories', 0),
        'max_calories': request.args.get('max_calories', 1000),
        'min_protein': request.args.get('min_protein', 0),
        'max_protein': request.args.get('max_protein', 100),
        'min_carbs': request.args.get('min_carbs', 0),
        'max_carbs': request.args.get('max_carbs', 100),
        'min_fat': request.args.get('min_fat', 0),
        'max_fat': request.args.get('max_fat', 100)
    }
    posts_data = get_recipes(query_params)
    if isinstance(posts_data, list):
        posts = posts_data
    elif isinstance(posts_data, dict) and 'data' in posts_data:
        posts = posts_data['data']
    else:
        posts = []
    return render_template('index.html', posts=posts)

@app.route('/classify_recipe', methods=['POST'])
def classify_recipe():
    recipe_id = request.form.get('recipe_id', '')
    # Simulated classification based on recipe id (API-specific logic might be needed)
    recipe_type = 'Main Course' if int(recipe_id) % 2 == 0 else 'Dessert'
    return render_template('index.html', recipe_type=recipe_type)

@app.route('/generate_meal_plan', methods=['POST'])
def generate_meal_plan():
    # Simulated meal plan generation
    meal_plan = [
        {'title': 'Breakfast Tacos', 'meal': 'Breakfast'},
        {'title': 'Guacamole Salad', 'meal': 'Lunch'},
        {'title': 'Chicken Enchiladas', 'meal': 'Dinner'}
    ]
    return render_template('index.html', meal_plan=meal_plan)

@app.route('/generate_shopping_list', methods=['POST'])
def generate_shopping_list():
    # Simulated shopping list generation
    shopping_list = [
        {'item': 'Tortillas', 'quantity': '10'},
        {'item': 'Avocados', 'quantity': '5'},
        {'item': 'Chicken Breast', 'quantity': '2 pounds'}
    ]
    return render_template('index.html', shopping_list=shopping_list)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
