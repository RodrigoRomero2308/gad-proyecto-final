from decimal import Decimal
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from requests.compat import quote
from db import similarity_search
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route("/health", methods=["GET"])
def health():
    return "ok"

@app.route("/get_bird_images", methods=["GET"])
def get_bird_images():
    bird_name = request.args.get("bird_name")
    if not bird_name:
        return jsonify({'error': "No bird name sent in request"}), 404
    
    pixabay_api_key = os.getenv("PIXABAY_API_KEY")

    if not pixabay_api_key:
        print('No pixabay_api_key found')
        return jsonify({'error': 'Internal server error'}), 500

    url = f"https://pixabay.com/api/?key={pixabay_api_key}&q=bird+{quote(bird_name)}&image_type=photo&orientation=horizontal&safesearch=true&per_page=3"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for non-200 status codes
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching images: {e}")
        return jsonify({"error": "Failed to fetch images"}), 500

@app.route('/search_for_songs', methods=['POST'])
def search_for_songs():
    if request.method == 'POST':
        
        mp3_file = request.files['file']
        radius = Decimal(request.form['radius'])

        if not os.path.exists('songs'):
            os.makedirs('songs')

        try:
            filepath = os.path.join('songs', mp3_file.filename)
            mp3_file.save(filepath)

            result = similarity_search(filepath, radius)

            os.remove(filepath)

            return jsonify(result)

        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # app.run(debug=True, host="0.0.0.0")
    from waitress import serve
    serve(app=app, host="0.0.0.0", port=5000)