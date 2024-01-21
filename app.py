from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

def fetch_random_recipe():
    endpoint = 'https://www.themealdb.com/api/json/v1/1/random.php'
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        data = response.json()
        return data['meals'][0] if 'meals' in data and data['meals'] else None
    except requests.exceptions.RequestException as e:
        print(f'Failed to fetch random recipe - {str(e)}')
        return None

@app.route('/recipes', methods=['GET'])
def get_recipes():
    try:
        recipe = fetch_random_recipe()
        if recipe:
            return jsonify({'recipes': [recipe]})
        else:
            return jsonify({'error': 'No recipe found'}), 404
    except Exception as e:
        print(f'An error occurred - {str(e)}')
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
