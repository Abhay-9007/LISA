from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
#import os

app = Flask(__name__, static_folder=".")
CORS(app)  # Allow all origins for debugging

try:
    from model import model
except ImportError as e:
    print(f"Failed to import model: {e}")
    def model(input_text):
        return f"Error: model not available, using fallback: {input_text.upper()}"  # Fallback

@app.route('/')
def serve_frontend():
    return send_from_directory(".", "index.html")  # serve index.html from current folder

@app.route('/process', methods=['POST'])
def process():
    try:
        data = request.json
        if not data or 'input' not in data:
            return jsonify({'error': 'No input provided'}), 400
        user_input = data.get('input', '')
        output = model(user_input)
        return jsonify({'output': str(output)})
    except Exception as e:
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(port=5000, host='0.0.0.0')  # No auto-reload
