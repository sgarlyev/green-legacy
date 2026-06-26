// ── i18n ──────────────────────────────────────────────────────────────────────
const TRANSLATIONS = {
  en: {
    nav_identify: 'Identify',
    nav_collection: 'Collection',
    nav_about: 'About',
    hero_title: 'Discover the Birds of Turkmenistan',
    hero_subtitle: 'Upload a photo and our AI will identify the bird and share its story.',
    upload_label: 'Drag & drop a bird photo here',
    upload_sub: 'or click to browse',
    upload_btn: 'Choose Photo',
    change_photo: 'Change Photo',
    identify_btn: 'Identify Bird',
    analyzing: 'Analyzing your photo...',
    tab_facts: 'Facts',
    tab_habitat: 'Habitat',
    tab_diet: 'Diet',
    tab_threats: 'Threats',
    tab_help: 'How to Help',
    new_photo: 'Identify Another Bird',
    retry: 'Try Again',
    collection_title: 'Bird Collection',
    collection_sub: '11 species found in Turkmenistan',
    about_title: 'About Green Legacy',
    about_p1: 'Green Legacy is an educational bird identification project focused on the birds of Turkmenistan. Our AI model is trained on photos of 11 common species found across the country.',
    about_p2: 'The project aims to connect people with local wildlife and inspire conservation action. By learning to recognize the birds around us, we build a deeper appreciation for the natural world.',
    stat_species: 'Species',
    stat_languages: 'Languages',
    stat_powered: 'Powered',
    tech_title: 'Technology',
    tech_1: 'TensorFlow Lite — on-device AI inference',
    tech_2: 'MobileNetV2 — efficient image classification',
    tech_3: 'Flask — Python web backend',
    tech_4: 'Trained on photos of Turkmenistan birds',
    footer: 'Green Legacy · Birds of Turkmenistan · Educational Project',
    confidence_label: 'confidence',
    modal_facts: 'Interesting Facts',
    modal_habitat: 'Habitat',
    modal_diet: 'Diet',
    modal_threats: 'Threats',
    modal_help: 'How to Help',
  },
  ru: {
    nav_identify: 'Определить',
    nav_collection: 'Коллекция',
    nav_about: 'О проекте',
    hero_title: 'Откройте для себя птиц Туркменистана',
    hero_subtitle: 'Загрузите фото, и наш ИИ определит птицу и расскажет о ней.',
    upload_label: 'Перетащите фото птицы сюда',
    upload_sub: 'или нажмите, чтобы выбрать',
    upload_btn: 'Выбрать фото',
    change_photo: 'Изменить фото',
    identify_btn: 'Определить птицу',
    analyzing: 'Анализирую фотографию...',
    tab_facts: 'Факты',
    tab_habitat: 'Среда обитания',
    tab_diet: 'Питание',
    tab_threats: 'Угрозы',
    tab_help: 'Как помочь',
    new_photo: 'Определить другую птицу',
    retry: 'Попробовать снова',
    collection_title: 'Коллекция птиц',
    collection_sub: '11 видов, встречающихся в Туркменистане',
    about_title: 'О проекте Green Legacy',
    about_p1: 'Green Legacy — образовательный проект по определению птиц Туркменистана. Наша ИИ-модель обучена на фотографиях 11 распространённых видов.',
    about_p2: 'Проект стремится связать людей с местной дикой природой и вдохновить на природоохранные действия.',
    stat_species: 'Видов',
    stat_languages: 'Языка',
    stat_powered: 'На ИИ',
    tech_title: 'Технологии',
    tech_1: 'TensorFlow Lite — вывод ИИ на устройстве',
    tech_2: 'MobileNetV2 — классификация изображений',
    tech_3: 'Flask — бэкенд на Python',
    tech_4: 'Обучено на фото птиц Туркменистана',
    footer: 'Green Legacy · Птицы Туркменистана · Образовательный проект',
    confidence_label: 'уверенность',
    modal_facts: 'Интересные факты',
    modal_habitat: 'Среда обитания',
    modal_diet: 'Питание',
    modal_threats: 'Угрозы',
    modal_help: 'Как помочь',
  },
  tk: {
    nav_identify: 'Kesgitlemek',
    nav_collection: 'Kolleksiýa',
    nav_about: 'Barada',
    hero_title: 'Türkmenistanyň Guşlaryny Açyň',
    hero_subtitle: 'Surat ýükläň, emeli aňymyz guşy kesgitlesin we onuň barada gürrüň bersin.',
    upload_label: 'Guş suratyny şu ýere süýräň',
    upload_sub: 'ýa-da saýlamak üçin basyň',
    upload_btn: 'Surat Saýlaň',
    change_photo: 'Suraty Çalyşyň',
    identify_btn: 'Guşy Kesgitle',
    analyzing: 'Suratyňyz derňelýär...',
    tab_facts: 'Faktlar',
    tab_habitat: 'Ýaşaýyş Ýeri',
    tab_diet: 'Iýmitleniş',
    tab_threats: 'Howplar',
    tab_help: 'Nädip Kömek Etmeli',
    new_photo: 'Başga Guşy Kesgitle',
    retry: 'Täzeden Synanyşmak',
    collection_title: 'Guş Kolleksiýasy',
    collection_sub: 'Türkmenistanda duşulýan 11 görnüş',
    about_title: 'Green Legacy Barada',
    about_p1: 'Green Legacy Türkmenistanyň guşlaryny kesgitlemek boýunça bilim taslamasy. Emeli aň modelimiz ýurtda duşulýan 11 ýaýran görnüşiň suratlary esasynda öwredildi.',
    about_p2: 'Taslama adamlary ýerli ýabany tebigat bilen baglanyşdyrmaga we tebigaty goramak hereketlerini ruhlandyrmaga gönükdirilendir.',
    stat_species: 'Görnüş',
    stat_languages: 'Dil',
    stat_powered: 'AI',
    tech_title: 'Tehnologiýa',
    tech_1: 'TensorFlow Lite — enjamda AI çaklamasy',
    tech_2: 'MobileNetV2 — surat klassifikasiýasy',
    tech_3: 'Flask — Python web backend',
    tech_4: 'Türkmenistanyň guş suratlary esasynda öwredildi',
    footer: 'Green Legacy · Türkmenistanyň Guşlary · Bilim Taslamasy',
    confidence_label: 'ygtybarlylyk',
    modal_facts: 'Gyzykly Faktlar',
    modal_habitat: 'Ýaşaýyş Ýeri',
    modal_diet: 'Iýmitleniş',
    modal_threats: 'Howplar',
    modal_help: 'Nädip Kömek Etmeli',
  }
};

let currentLang = 'en';
let birdsData = [];
let selectedFile = null;
let currentBird = null;
let currentTab = 'facts';

// ── Language ─────────────────────────────────────────────────────────────────
function t(key) {
  return TRANSLATIONS[currentLang][key] || TRANSLATIONS.en[key] || key;
}

function applyTranslations() {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    el.textContent = t(key);
  });
  // Re-render result if visible
  if (currentBird && document.getElementById('result-card').style.display !== 'none') {
    renderResult(currentBird, lastConfidence);
  }
  // Re-render tab content
  if (currentBird) {
    renderTabContent(currentTab);
  }
}

function setLanguage(lang) {
  currentLang = lang;
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.lang === lang);
  });
  applyTranslations();
  if (document.getElementById('view-collection').style.display !== 'none') {
    renderBirdGrid();
  }
}

// ── Navigation ────────────────────────────────────────────────────────────────
function showView(view) {
  ['home', 'collection', 'about'].forEach(v => {
    const el = document.getElementById(`view-${v}`);
    if (el) el.style.display = v === view ? '' : 'none';
  });
  document.querySelectorAll('.nav-btn').forEach(btn => {
    const id = btn.id.replace('nav-', '');
    btn.classList.toggle('active', id === view || (view === 'home' && id === 'identify'));
  });
  if (view === 'collection') {
    renderBirdGrid();
  }
}

// ── File Upload ───────────────────────────────────────────────────────────────
function initUpload() {
  const area = document.getElementById('upload-area');
  const input = document.getElementById('file-input');
  const chooseBtn = document.getElementById('choose-btn');
  const changeBtn = document.getElementById('change-btn');

  chooseBtn.addEventListener('click', e => { e.stopPropagation(); input.click(); });
  changeBtn.addEventListener('click', e => { e.stopPropagation(); input.click(); });
  area.addEventListener('click', () => { if (!selectedFile) input.click(); });

  input.addEventListener('change', () => {
    if (input.files[0]) setFile(input.files[0]);
  });

  area.addEventListener('dragover', e => {
    e.preventDefault();
    area.classList.add('drag-over');
  });
  area.addEventListener('dragleave', () => area.classList.remove('drag-over'));
  area.addEventListener('drop', e => {
    e.preventDefault();
    area.classList.remove('drag-over');
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) setFile(file);
  });
}

function setFile(file) {
  selectedFile = file;
  const reader = new FileReader();
  reader.onload = e => {
    document.getElementById('preview-img').src = e.target.result;
    document.getElementById('upload-idle').style.display = 'none';
    document.getElementById('upload-preview').style.display = 'flex';
    document.getElementById('identify-btn').disabled = false;
  };
  reader.readAsDataURL(file);
  // Hide previous results
  hideAll(['loading-state', 'result-card', 'error-state']);
}

// ── Identify ──────────────────────────────────────────────────────────────────
let lastConfidence = 0;

async function identify() {
  if (!selectedFile) return;

  hideAll(['result-card', 'error-state']);
  show('loading-state');
  document.getElementById('identify-btn').disabled = true;

  const formData = new FormData();
  formData.append('image', selectedFile);

  try {
    const res = await fetch('/api/identify', { method: 'POST', body: formData });
    const data = await res.json();

    hide('loading-state');

    if (!res.ok || data.error) {
      showError(data.error || 'Identification failed. Please try again.');
      return;
    }

    currentBird = data.bird;
    lastConfidence = data.confidence;
    renderResult(data.bird, data.confidence, data.demo);
    show('result-card');
    document.getElementById('result-card').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  } catch (err) {
    hide('loading-state');
    showError('Network error. Please check your connection.');
  } finally {
    document.getElementById('identify-btn').disabled = false;
  }
}

function renderResult(bird, confidence, demo = false) {
  const lang = currentLang;
  document.getElementById('result-common-name').textContent = bird.name[lang] || bird.name.en;
  document.getElementById('result-sci-name').textContent = bird.scientific_name;
  document.getElementById('result-status').textContent = bird.status;
  document.getElementById('result-description').textContent =
    (bird.description && bird.description[lang]) || bird.description?.en || '';
  document.getElementById('confidence-badge').textContent =
    demo ? `DEMO MODE` : `${confidence}% ${t('confidence_label')}`;

  const img = document.getElementById('result-bird-img');
  img.src = bird.image;
  img.onerror = () => { img.src = getPlaceholderSvg(bird.id); };

  // Activate tabs
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.tab === currentTab);
    btn.addEventListener('click', function() {
      currentTab = this.dataset.tab;
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      renderTabContent(currentTab);
    });
  });

  renderTabContent(currentTab);
}

function renderTabContent(tab) {
  if (!currentBird) return;
  const lang = currentLang;
  const el = document.getElementById('tab-content');

  if (tab === 'facts') {
    const items = currentBird.facts?.[lang] || currentBird.facts?.en || [];
    el.innerHTML = `<ul>${items.map(f => `<li>${f}</li>`).join('')}</ul>`;
  } else {
    const text = currentBird[tab]?.[lang] || currentBird[tab]?.en || '';
    el.innerHTML = `<p>${text}</p>`;
  }
}

// ── Bird Grid ─────────────────────────────────────────────────────────────────
async function loadBirds() {
  try {
    const res = await fetch('/api/birds');
    birdsData = await res.json();
  } catch (e) {
    console.error('Failed to load birds:', e);
  }
}

function renderBirdGrid() {
  const grid = document.getElementById('bird-grid');
  if (!grid || birdsData.length === 0) return;
  const lang = currentLang;

  grid.innerHTML = birdsData.map(bird => {
    const name = bird.name[lang] || bird.name.en;
    return `
      <div class="bird-card" onclick="openModal('${bird.id}')">
        <div class="bird-card-img">
          <img src="${bird.image}" alt="${name}"
               onerror="this.parentElement.innerHTML='${getBirdEmoji(bird.id)}'">
        </div>
        <div class="bird-card-body">
          <div class="bird-card-name">${name}</div>
          <div class="bird-card-sci">${bird.scientific_name}</div>
          <span class="bird-card-status">${bird.status}</span>
        </div>
      </div>`;
  }).join('');
}

// ── Modal ─────────────────────────────────────────────────────────────────────
function openModal(birdId) {
  const bird = birdsData.find(b => b.id === birdId);
  if (!bird) return;
  const lang = currentLang;
  const name = bird.name[lang] || bird.name.en;

  const facts = (bird.facts?.[lang] || bird.facts?.en || [])
    .map(f => `<li>${f}</li>`).join('');

  document.getElementById('modal-content').innerHTML = `
    <div class="modal-header">
      <img src="${bird.image}" alt="${name}"
           onerror="this.src='${getPlaceholderSvgInline(bird.id)}'">
      <div>
        <h2>${name}</h2>
        <p class="sci">${bird.scientific_name}</p>
        <span class="status-badge">${bird.status}</span>
      </div>
    </div>
    <div class="modal-body">
      <p>${bird.description?.[lang] || bird.description?.en || ''}</p>
      <div class="modal-section">
        <h3>${t('modal_facts')}</h3>
        <ul>${facts}</ul>
      </div>
      <div class="modal-section">
        <h3>${t('modal_habitat')}</h3>
        <p>${bird.habitat?.[lang] || bird.habitat?.en || ''}</p>
      </div>
      <div class="modal-section">
        <h3>${t('modal_diet')}</h3>
        <p>${bird.diet?.[lang] || bird.diet?.en || ''}</p>
      </div>
      <div class="modal-section">
        <h3>${t('modal_threats')}</h3>
        <p>${bird.threats?.[lang] || bird.threats?.en || ''}</p>
      </div>
      <div class="modal-section">
        <h3>${t('modal_help')}</h3>
        <p>${bird.conservation?.[lang] || bird.conservation?.en || ''}</p>
      </div>
    </div>`;

  document.getElementById('modal-overlay').style.display = 'flex';
  document.body.style.overflow = 'hidden';
}

function closeModal() {
  document.getElementById('modal-overlay').style.display = 'none';
  document.body.style.overflow = '';
}

// ── Utilities ─────────────────────────────────────────────────────────────────
function show(id) { const el = document.getElementById(id); if (el) el.style.display = ''; }
function hide(id) { const el = document.getElementById(id); if (el) el.style.display = 'none'; }
function hideAll(ids) { ids.forEach(hide); }

function showError(msg) {
  document.getElementById('error-message').textContent = msg;
  show('error-state');
}

function getPlaceholderSvg(id) {
  return `data:image/svg+xml,${encodeURIComponent(
    `<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
      <rect width="100" height="100" fill="#D8F3DC"/>
      <text x="50" y="60" text-anchor="middle" font-size="40">${getBirdEmoji(id)}</text>
    </svg>`
  )}`;
}

function getPlaceholderSvgInline(id) {
  return getPlaceholderSvg(id).replace(/"/g, "'");
}

function getBirdEmoji(id) {
  const emojis = {
    rock_pigeon: '🕊️', house_sparrow: '🐦', common_myna: '🐦',
    eurasian_collared_dove: '🕊️', mallard: '🦆', eurasian_coot: '🦢',
    common_kestrel: '🦅', black_kite: '🦅', chukar_partridge: '🐔',
    common_pheasant: '🦃', rook: '🐦‍⬛'
  };
  return emojis[id] || '🐦';
}

// ── Init ──────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', async () => {
  // Language buttons
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.addEventListener('click', () => setLanguage(btn.dataset.lang));
  });

  // Identify button
  document.getElementById('identify-btn').addEventListener('click', identify);

  // New photo button
  document.getElementById('new-photo-btn').addEventListener('click', () => {
    selectedFile = null;
    currentBird = null;
    currentTab = 'facts';
    document.getElementById('upload-idle').style.display = '';
    document.getElementById('upload-preview').style.display = 'none';
    document.getElementById('identify-btn').disabled = true;
    document.getElementById('file-input').value = '';
    hideAll(['result-card', 'error-state', 'loading-state']);
    document.getElementById('upload-area').scrollIntoView({ behavior: 'smooth' });
  });

  // Retry button
  document.getElementById('retry-btn').addEventListener('click', () => {
    hide('error-state');
  });

  // Keyboard: close modal with Escape
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeModal();
  });

  initUpload();
  await loadBirds();
  applyTranslations();
});
