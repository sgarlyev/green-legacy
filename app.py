import os, json, random, io
import numpy as np
from flask import Flask, request, jsonify, render_template, send_from_directory
from PIL import Image

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

MODELS_DIR       = os.path.join(os.path.dirname(__file__), 'models')
MODEL_PT_PATH    = os.path.join(MODELS_DIR, 'bird_classifier.pt')
CLASS_NAMES_PATH = os.path.join(MODELS_DIR, 'class_names.json')

with open(CLASS_NAMES_PATH) as f:
    CLASS_NAMES = json.load(f)

with open(os.path.join(os.path.dirname(__file__), 'birds.json')) as f:
    BIRDS_DATA = {b['id']: b for b in json.load(f)['birds']}

model = None
MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
STD  = np.array([0.229, 0.224, 0.225], dtype=np.float32)

def load_model():
    global model
    if not os.path.exists(MODEL_PT_PATH):
        print("bird_classifier.pt не найдена — ДЕМО режим")
        return False
    try:
        import torch
        model = torch.jit.load(MODEL_PT_PATH, map_location='cpu')
        model.eval()
        print("Модель загружена успешно")
        return True
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        return False

MODEL_LOADED = load_model()

def predict(image_bytes):
    import torch
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB').resize((224, 224), Image.LANCZOS)
    arr = np.array(img, dtype=np.float32) / 255.0
    arr = (arr - MEAN) / STD
    tensor = torch.from_numpy(arr.transpose(2, 0, 1)).unsqueeze(0)
    with torch.no_grad():
        out = model(tensor)[0]
        probs = torch.softmax(out, dim=0).numpy()
    idx = int(probs.argmax())
    return CLASS_NAMES[idx], float(probs[idx])

def identify_demo(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB').resize((32, 32))
    arr = np.array(img, dtype=np.float32)
    seed = int(arr.mean() * 1000 + arr.std() * 100) % len(CLASS_NAMES)
    return CLASS_NAMES[seed], round(random.uniform(0.72, 0.91), 3)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/identify', methods=['POST'])
def identify():
    if 'image' not in request.files:
        return jsonify({'error': 'Фото не загружено'}), 400
    file = request.files['image']
    if not file.filename:
        return jsonify({'error': 'Пустое имя файла'}), 400
    allowed = {'jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp'}
    ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
    if ext not in allowed:
        return jsonify({'error': 'Неподдерживаемый формат'}), 400

    image_bytes = file.read()
    demo = False

    if MODEL_LOADED:
        try:
            bird_id, confidence = predict(image_bytes)
        except Exception as e:
            print(f"Predict error: {e}")
            bird_id, confidence = identify_demo(image_bytes)
            demo = True
    else:
        bird_id, confidence = identify_demo(image_bytes)
        demo = True

    bird = BIRDS_DATA.get(bird_id)
    if not bird:
        return jsonify({'error': f'Неизвестный вид: {bird_id}'}), 500

    return jsonify({
        'bird_id': bird_id,
        'confidence': round(confidence * 100, 1),
        'bird': bird,
        'demo': demo,
    })

@app.route('/api/birds')
def get_birds():
    return jsonify(list(BIRDS_DATA.values()))

@app.route('/api/bird/<bird_id>')
def get_bird(bird_id):
    bird = BIRDS_DATA.get(bird_id)
    if not bird:
        return jsonify({'error': 'Не найдено'}), 404
    return jsonify(bird)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
