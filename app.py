import os, json, random, io
import requests
import numpy as np
from flask import Flask, request, jsonify, render_template, send_from_directory
from PIL import Image

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Hugging Face — готовая модель на 500+ видов птиц
HF_API_URL = "https://api-inference.huggingface.co/models/chriamue/bird-species-classifier"
HF_TOKEN   = os.environ.get("HF_TOKEN", "")   # необязательно, без него тоже работает

# Маппинг: как модель называет наших птиц → наш ID
BIRD_NAMES_MAP = {
    # rock pigeon / rock dove
    "rock dove": "rock_pigeon", "columbia livia": "rock_pigeon",
    "common pigeon": "rock_pigeon", "rock pigeon": "rock_pigeon",
    # house sparrow
    "house sparrow": "house_sparrow",
    # common myna
    "common myna": "common_myna", "common mynah": "common_myna",
    "common myna bird": "common_myna",
    # eurasian collared dove
    "eurasian collared dove": "eurasian_collared_dove",
    "collared dove": "eurasian_collared_dove",
    # mallard
    "mallard": "mallard", "mallard duck": "mallard",
    # eurasian coot
    "eurasian coot": "eurasian_coot", "coot": "eurasian_coot",
    "common coot": "eurasian_coot",
    # common kestrel
    "common kestrel": "common_kestrel", "kestrel": "common_kestrel",
    "eurasian kestrel": "common_kestrel",
    # black kite
    "black kite": "black_kite",
    # chukar partridge
    "chukar partridge": "chukar_partridge", "chukar": "chukar_partridge",
    # common pheasant
    "common pheasant": "common_pheasant", "pheasant": "common_pheasant",
    "ring-necked pheasant": "common_pheasant",
    # rook
    "rook": "rook",
}

CLASS_NAMES_PATH = os.path.join(os.path.dirname(__file__), 'models', 'class_names.json')
with open(CLASS_NAMES_PATH) as f:
    CLASS_NAMES = json.load(f)

with open(os.path.join(os.path.dirname(__file__), 'birds.json')) as f:
    BIRDS_DATA = {b['id']: b for b in json.load(f)['birds']}


_last_hf_results = []  # глобально сохраняем последний ответ

def identify_via_hf(image_bytes):
    global _last_hf_results
    headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}
    try:
        resp = requests.post(HF_API_URL, headers=headers,
                             data=image_bytes, timeout=30)
        if resp.status_code == 200:
            results = resp.json()
            _last_hf_results = results[:10] if isinstance(results, list) else []
            if isinstance(results, list) and results:
                for item in results[:15]:
                    label = item.get("label", "").lower().strip()
                    score = item.get("score", 0)
                    bird_id = BIRD_NAMES_MAP.get(label)
                    if bird_id:
                        return bird_id, score
                    for key, bid in BIRD_NAMES_MAP.items():
                        if key in label or label in key:
                            return bid, score
        else:
            _last_hf_results = [{"error": resp.status_code, "text": resp.text[:300]}]
        return None, 0
    except Exception as e:
        _last_hf_results = [{"exception": str(e)}]
        return None, 0


def identify_demo(image_bytes):
    """Демо-режим: псевдослучайный результат на основе цвета фото."""
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
    bird_id, confidence = identify_via_hf(image_bytes)
    demo = False

    if not bird_id:
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
        'debug_hf': _last_hf_results,
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
