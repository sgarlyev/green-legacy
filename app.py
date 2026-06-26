import os
import json
import random
import numpy as np
from flask import Flask, request, jsonify, render_template, send_from_directory
from PIL import Image
import io

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload

MODELS_DIR = os.path.join(os.path.dirname(__file__), 'models')
MODEL_PATH = os.path.join(MODELS_DIR, 'bird_classifier.tflite')
CLASS_NAMES_PATH = os.path.join(MODELS_DIR, 'class_names.json')

with open(CLASS_NAMES_PATH) as f:
    CLASS_NAMES = json.load(f)

BIRDS_PATH = os.path.join(os.path.dirname(__file__), 'birds.json')
with open(BIRDS_PATH) as f:
    BIRDS_DATA = {b['id']: b for b in json.load(f)['birds']}

interpreter = None

def load_model():
    global interpreter
    if not os.path.exists(MODEL_PATH):
        print("bird_classifier.tflite not found — running in DEMO mode")
        return False
    try:
        try:
            import tflite_runtime.interpreter as tflite
            interpreter = tflite.Interpreter(model_path=MODEL_PATH)
        except ImportError:
            import tensorflow as tf
            interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
        interpreter.allocate_tensors()
        print("Model loaded successfully")
        return True
    except Exception as e:
        print(f"Model load error: {e}")
        return False

MODEL_LOADED = load_model()

def preprocess_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img = img.resize((224, 224), Image.LANCZOS)
    arr = np.array(img, dtype=np.float32)
    arr = (arr / 127.5) - 1.0  # MobileNetV2 preprocessing
    return np.expand_dims(arr, axis=0)

def predict(image_bytes):
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    input_data = preprocess_image(image_bytes)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])[0]
    idx = int(np.argmax(output))
    confidence = float(output[idx])
    if confidence > 1.0 or confidence < 0.0:
        output = np.exp(output - np.max(output))
        output /= output.sum()
        idx = int(np.argmax(output))
        confidence = float(output[idx])
    return CLASS_NAMES[idx], confidence

def predict_demo(image_bytes):
    # Use pixel statistics to pick a semi-deterministic result for demo
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img = img.resize((64, 64))
    arr = np.array(img, dtype=np.float32)
    seed = int(arr.mean() * 1000 + arr.std() * 100) % len(CLASS_NAMES)
    bird_id = CLASS_NAMES[seed]
    confidence = round(random.uniform(72, 91), 1)
    return bird_id, confidence

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def status():
    return jsonify({'model_loaded': MODEL_LOADED, 'demo_mode': not MODEL_LOADED})

@app.route('/api/identify', methods=['POST'])
def identify():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400
    allowed = {'jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp'}
    ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
    if ext not in allowed:
        return jsonify({'error': 'Unsupported file type'}), 400

    image_bytes = file.read()

    if MODEL_LOADED:
        bird_id, confidence = predict(image_bytes)
        demo = False
    else:
        bird_id, confidence = predict_demo(image_bytes)
        demo = True

    bird = BIRDS_DATA.get(bird_id)
    if not bird:
        return jsonify({'error': f'Unknown bird ID: {bird_id}'}), 500

    return jsonify({
        'bird_id': bird_id,
        'confidence': round(confidence, 1),
        'bird': bird,
        'demo': demo
    })

@app.route('/api/birds')
def get_birds():
    return jsonify(list(BIRDS_DATA.values()))

@app.route('/api/bird/<bird_id>')
def get_bird(bird_id):
    bird = BIRDS_DATA.get(bird_id)
    if not bird:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(bird)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
