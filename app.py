import os, json, random, io
import requests
import numpy as np
from flask import Flask, request, jsonify, render_template, send_from_directory
from PIL import Image

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# iNaturalist Computer Vision API — обучена на миллионах фото дикой природы
INAT_API = "https://api.inaturalist.org/v1/computervision/score_image"
HEADERS  = {"User-Agent": "GreenLegacy/1.0 (garlyevserdar1604@gmail.com)"}

# Маппинг: научное название → наш ID
SCIENTIFIC_MAP = {
    "milvus migrans": "black_kite",
    "alectoris chukar": "chukar_partridge",
    "falco tinnunculus": "common_kestrel",
    "acridotheres tristis": "common_myna",
    "phasianus colchicus": "common_pheasant",
    "streptopelia decaocto": "eurasian_collared_dove",
    "fulica atra": "eurasian_coot",
    "passer domesticus": "house_sparrow",
    "anas platyrhynchos": "mallard",
    "columba livia": "rock_pigeon",
    "corvus frugilegus": "rook",
}

# Маппинг: ключевое слово в названии → наш ID (для похожих видов)
KEYWORD_MAP = [
    # Майна и похожие
    (["myna", "mynah", "acridotheres", "starling", "myna bird"], "common_myna"),
    # Голубь и горлица
    (["pigeon", "dove", "columba", "feral"], "rock_pigeon"),
    # Кольчатая горлица конкретно
    (["collared dove", "collared-dove", "streptopelia", "turtle dove"], "eurasian_collared_dove"),
    # Воробей
    (["sparrow", "passer"], "house_sparrow"),
    # Кряква и утки
    (["mallard", "duck", "anas", "drake", "teal"], "mallard"),
    # Лысуха
    (["coot", "fulica", "moorhen", "gallinule", "waterhen"], "eurasian_coot"),
    # Пустельга и соколы
    (["kestrel", "falco", "falcon", "hobby"], "common_kestrel"),
    # Коршун
    (["kite", "milvus", "black kite"], "black_kite"),
    # Кеклик
    (["chukar", "partridge", "alectoris", "francolin", "quail"], "chukar_partridge"),
    # Фазан
    (["pheasant", "phasianus", "peafowl"], "common_pheasant"),
    # Грач и вороны
    (["rook", "corvus", "crow", "raven", "jackdaw", "chough", "magpie"], "rook"),
]

CLASS_NAMES_PATH = os.path.join(os.path.dirname(__file__), 'models', 'class_names.json')
with open(CLASS_NAMES_PATH) as f:
    CLASS_NAMES = json.load(f)

with open(os.path.join(os.path.dirname(__file__), 'birds.json')) as f:
    BIRDS_DATA = {b['id']: b for b in json.load(f)['birds']}


def identify_via_inat(image_bytes):
    """Отправляет фото в iNaturalist CV и ищет наших 11 птиц в топ-20."""
    try:
        # Сжимаем для быстрой отправки
        img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        img.thumbnail((800, 800), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format='JPEG', quality=88)
        buf.seek(0)

        resp = requests.post(
            INAT_API,
            headers=HEADERS,
            files={"image": ("photo.jpg", buf, "image/jpeg")},
            timeout=20,
        )

        if resp.status_code != 200:
            print(f"iNat error: {resp.status_code} {resp.text[:200]}")
            return None, 0

        data = resp.json()
        results = data.get("results", [])

        # Перебираем топ-30 результатов iNaturalist
        for item in results[:30]:
            taxon = item.get("taxon", {})
            score = item.get("combined_score", 0)
            sci    = taxon.get("name", "").lower()
            common = taxon.get("preferred_common_name", "").lower()
            search = f"{sci} {common}"

            # Точное научное название
            if sci in SCIENTIFIC_MAP:
                return SCIENTIFIC_MAP[sci], score

            # Ключевые слова — от конкретных к общим
            for keywords, bid in KEYWORD_MAP:
                if any(kw in search for kw in keywords):
                    return bid, score

        top3 = [(r.get('taxon',{}).get('name'), r.get('taxon',{}).get('preferred_common_name'), r.get('combined_score')) for r in results[:3]]
        print(f"iNat no match, top3: {top3}")
        return None, 0

    except Exception as e:
        print(f"iNat error: {e}")
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
    bird_id, confidence = identify_via_inat(image_bytes)
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
