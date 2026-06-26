import os, json, random, io, base64
import requests
import numpy as np
from flask import Flask, request, jsonify, render_template, send_from_directory
from PIL import Image

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# CLIP zero-shot — даём ровно наши 11 видов, модель выбирает ближайший
CLIP_API = "https://api-inference.huggingface.co/models/openai/clip-vit-large-patch14"
HF_TOKEN = os.environ.get("HF_TOKEN", "")

# Описания для CLIP (чем точнее описание, тем лучше результат)
BIRD_LABELS = {
    "rock_pigeon":             "a rock pigeon or rock dove, grey bird with iridescent neck",
    "house_sparrow":           "a house sparrow, small brown bird with streaked back",
    "common_myna":             "a common myna bird, black and brown with yellow beak and eye patch",
    "eurasian_collared_dove":  "a eurasian collared dove, pale beige dove with black neck collar",
    "mallard":                 "a mallard duck, green headed duck or brown female duck on water",
    "eurasian_coot":           "a eurasian coot, all black water bird with white forehead shield",
    "common_kestrel":          "a common kestrel falcon, hovering bird of prey with spotted brown plumage",
    "black_kite":              "a black kite, dark brown raptor with forked tail soaring",
    "chukar_partridge":        "a chukar partridge, grey bird with black and white striped face",
    "common_pheasant":         "a common pheasant, colorful bird with long tail, red face wattles",
    "rook":                    "a rook, all black crow with bare pale face at base of beak",
}

CLASS_NAMES_PATH = os.path.join(os.path.dirname(__file__), 'models', 'class_names.json')
with open(CLASS_NAMES_PATH) as f:
    CLASS_NAMES = json.load(f)

with open(os.path.join(os.path.dirname(__file__), 'birds.json')) as f:
    BIRDS_DATA = {b['id']: b for b in json.load(f)['birds']}


def identify_via_clip(image_bytes):
    """CLIP zero-shot: выбирает из наших 11 птиц ту, что лучше всего описывает фото."""
    try:
        # Сжимаем изображение для быстрой передачи
        img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        img.thumbnail((512, 512), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format='JPEG', quality=85)
        img_b64 = base64.b64encode(buf.getvalue()).decode()

        labels = list(BIRD_LABELS.keys())
        descriptions = list(BIRD_LABELS.values())

        headers = {"Content-Type": "application/json"}
        if HF_TOKEN:
            headers["Authorization"] = f"Bearer {HF_TOKEN}"

        payload = {
            "inputs": img_b64,
            "parameters": {"candidate_labels": descriptions}
        }

        resp = requests.post(CLIP_API, headers=headers,
                             json=payload, timeout=40)

        if resp.status_code == 200:
            results = resp.json()
            if isinstance(results, list) and results:
                # CLIP возвращает результаты по порядку candidate_labels
                top = results[0]
                top_desc = top.get("label", "")
                score = top.get("score", 0)
                # Находим bird_id по описанию
                for bird_id, desc in BIRD_LABELS.items():
                    if desc == top_desc:
                        return bird_id, score
                # Если не нашли точно — берём индекс
                for i, desc in enumerate(descriptions):
                    if desc == top_desc and i < len(labels):
                        return labels[i], score
        return None, 0
    except Exception as e:
        print(f"CLIP error: {e}")
        return None, 0


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
    bird_id, confidence = identify_via_clip(image_bytes)
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
