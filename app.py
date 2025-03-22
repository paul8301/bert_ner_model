from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from transformers import AutoTokenizer, TFAutoModelForTokenClassification
import tensorflow as tf
import json
import os

app = Flask(__name__)
auth = HTTPBasicAuth()

# Use environment variable for password or set a default
DEFAULT_PASSWORD = os.environ.get('API_PASSWORD', 'your_secure_password')

# Basic Authentication
users = {
    "admin": generate_password_hash(DEFAULT_PASSWORD)
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

# Load the saved model, tokenizer, and schema
MODEL_PATH = './ner_model'
model = TFAutoModelForTokenClassification.from_pretrained(MODEL_PATH)
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

# Load the schema
with open(os.path.join(MODEL_PATH, 'schema.json'), 'r') as f:
    schema = json.load(f)

# Recreate tag mappings
tag_index = {tag: i for i, tag in enumerate(schema)}
index_to_tag = {i: tag for tag, i in tag_index.items()}

# Root route to provide basic API information
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "NER Model API",
        "endpoints": {
            "/predict": "POST endpoint for Named Entity Recognition",
            "/schema": "GET endpoint to retrieve NER schema"
        }
    })

@app.route('/predict', methods=['POST'])
@auth.login_required
def predict():
    # Get input text from JSON request
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    
    text = data.get('text', '')
    
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    # Tokenize the input
    inputs = tokenizer(text, return_tensors="tf", padding=True, truncation=True)
    
    # Get model predictions
    outputs = model(inputs)
    predictions = tf.argmax(outputs.logits, axis=-1).numpy()[0]
    
    # Map predictions to original tokens
    tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
    
    # Filter out special tokens and map to entity tags
    results = []
    for token, pred in zip(tokens, predictions):
        if not token.startswith('##') and token not in ['[CLS]', '[SEP]']:
            results.append({
                'token': token,
                'entity': index_to_tag[pred]
            })
    
    return jsonify(results)

@app.route('/schema', methods=['GET'])
@auth.login_required
def get_schema():
    """Endpoint to retrieve the model's NER schema"""
    return jsonify(schema)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)