from decimal import Decimal
from flask import Flask, request, jsonify
from db import similarity_search
import os

app = Flask(__name__)

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
    app.run(debug=True)
