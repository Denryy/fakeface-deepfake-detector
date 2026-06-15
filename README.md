# FakeFace — Deepfake Detector

> Детектор и размеченный датасет для выявления **deepfake-рекламы** (поддельное лицо/голос
> в финансовых промо). Часть проекта **Media Fraud Watch + Shadow Graph** (Кейс 9).

![Python](https://img.shields.io/badge/Python-3.13-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-2.6%20%2B%20CUDA-ee4c2c)
![Dataset](https://img.shields.io/badge/dataset-150%20examples-success)
![Languages](https://img.shields.io/badge/languages-ru%20%7C%20kk%20%7C%20en-informational)

Система **не выносит вердикт** «это дипфейк». Она поднимает **объяснимые risk-сигналы**
(`possible_deepfake`, `synthetic_voice_suspected`, `lip_sync_anomaly`) и передаёт материал
аналитику. Главная ценность — *объяснимая цепочка доказательств, а не «AI сказал scam»*.

---

## ✨ Возможности

- 🎥 **Видео-детектор (ансамбль из 5 моделей)** — кадры (OpenCV) → лица → максимум по:
  3 ViT (`prithivMLmods`/`dima806`/`Wvolf`) + **NPR** (сгенерированные лица) + **DFDC** (selimsef, 7×B7, face-swap).
- 🎙️ **Голос-детектор** — извлечение аудио (ffmpeg) → Wav2Vec2 анти-спуфинг на GPU.
- 🌐 **Веб-UI** — загрузка видео в браузере → флаги, вероятности по моделям, вердикт.
- 🧩 **Stub-детектор** — лёгкая эвристика (stdlib) для разметки датасета и demo.
- 📊 **Датасет 150 примеров** (75 fake / 75 real), мультиязычный **ru / kk / en**, уникальные сценарии.
- 🔌 **Единый контракт** `media_anomalies` — встраивается в общий risk-конвейер без изменений.

---

## 🏗️ Архитектура

```
SOURCES.md (источники real/fake)
      │
      ▼
┌──────────────────────┐     ┌──────────────────────────────────────────────┐
│ fakeface_detector_   │     │ fakeface_detector_real (GPU)                 │
│ stub  (эвристика)    │     │  видео: OpenCV → ансамбль 5 моделей (max)    │
│                      │     │         3 ViT + NPR(generated) + DFDC(swap)  │
│                      │     │  аудио: ffmpeg → Wav2Vec2 (голос)            │
└──────────┬───────────┘     └──────────────────┬───────────────────────────┘
           │   общий контракт media_anomalies   │
           └──────────────────┬─────────────────┘
                              ▼
        deepfake_examples.jsonl  (150 размеченных записей)
                              ▼
        [risk engine] → [shadow graph] → explainable report
```

3 из 4 флагов в реальном детекторе считаются **по-настоящему** (`has_face`,
`possible_deepfake`, `synthetic_voice_suspected`); `lip_sync_anomaly` — план развития (SyncNet).

---

## 📊 Датасет

| | |
|---|---|
| Объём | **150** (75 fake / 75 real), 0 битых JSON, 0 дублей |
| Языки | **ru / kk / en** — распределены по уникальным сценариям (без дублей-переводов) |
| Источники | synthetic + публичные датасеты (FaceForensics++, FakeAVCeleb, DFDC, DF40, WildDeepfake, audio) |
| Сценарии | инвест-платформа, банк-CEO, крипто-бот, майнинг, казино, пирамида, розыгрыш, crypto giveaway + real |
| Формат | JSONL, одна запись на строку (схема ниже) |

> Каталог сценариев и метод разметки — в [`docs/fakeface_findings.md`](docs/fakeface_findings.md).

---

## 🚀 Быстрый старт

### Stub-детектор (без зависимостей)
```bash
python src/media/fakeface_detector_stub.py \
  --input data/raw/deepfake/SOURCES.md \
  --out   data/processed/deepfake_examples.jsonl
```

### Реальный детектор (GPU) — через [uv](https://docs.astral.sh/uv/)
```bash
# venv с доступом к системному torch (cu124) — лёгкая сборка, torch не дублируется
uv venv --system-site-packages
uv pip install -r requirements-detector.txt   # зависимости также в pyproject.toml

# анализ видео (видео + аудио)
.venv/Scripts/python src/media/fakeface_detector_real.py --video path/to/video.mp4
# --no-audio  — отключить аудио-ветку

# веб-UI (загрузка видео в браузере):
uv pip install ".[ui]"
.venv/Scripts/python src/media/detector_server.py   # → http://127.0.0.1:8000
```
ViT- и аудио-модели скачиваются с HuggingFace при первом запуске. NPR/DFDC — опциональные
(веса локальные, `vendor/`); без них ансамбль использует 3 ViT + голос.

#### Установка с нуля (другая машина, torch ещё не установлен)
Лёгкая сборка переиспользует системный `torch`. Если его нет — поставь **полный** стек:

```bash
# NVIDIA GPU + CUDA 12.4 (self-contained, скачает torch ~2.5ГБ)
uv venv
uv pip install ".[gpu]"                        # torch + torchvision (cu124)
uv pip install -r requirements-detector.txt    # opencv, transformers, soundfile, ...

# CPU-only (без GPU) — заменить индекс на cpu:
#   uv pip install torch==2.6.0 torchvision==0.21.0 --index-url https://download.pytorch.org/whl/cpu
```

> **Важно для воспроизводимости:** в основных `dependencies` (`pyproject.toml`) **нет**
> `torch` — он тяжёлый и привязан к платформе/CUDA. Для машины с уже установленным
> `torch` cu124 хватает лёгкой сборки выше (`--system-site-packages`); для чистой машины —
> ставь группу `gpu` (или CPU-вариант). Проверено на RTX 3050 6GB, torch 2.6+cu124.

> ⚠️ `transformers` 5.x требует `torch ≥ 2.7` — поэтому детектор использует
> `transformers==4.49` в отдельном venv (см. `requirements-detector.txt`).

---

## 📁 Структура

```
src/media/
  fakeface_detector_stub.py    # эвристический детектор (stdlib)
  fakeface_detector_real.py    # реальный детектор (OpenCV + ViT + Wav2Vec2, GPU)
data/
  raw/deepfake/SOURCES.md      # реестр источников (ссылки/метки, без тяжёлых видео)
  processed/deepfake_examples.jsonl   # итоговый датасет (150)
docs/
  fakeface_findings.md         # отчёт: источники, метод, детектор (§8), сценарии (§9)
  student6_brief.md            # исходное ТЗ зоны
requirements-detector.txt      # зависимости реального детектора
```

> Репозиторий также содержит **скаффолд-контракты** соседних модулей командного проекта
> (`src/parsers`, `src/extraction`, `src/risk`, `src/graph`, `src/app`) — интерфейсы и
> константы из ТЗ без бизнес-логики.

---

## 📋 Контракт данных (запись датасета)

```json
{
  "id": "deepfake_0001",
  "modality": "video",
  "language": "ru",
  "transcript": "Я инвестировал в эту платформу...",
  "entities": { "domains": ["invest-pro.example"], "telegram_usernames": ["@invest_mgr_1"], "...": [] },
  "media_anomalies": {
    "has_face": true, "possible_deepfake": true,
    "synthetic_voice_suspected": true, "lip_sync_anomaly": true
  },
  "risk_signals": ["possible_deepfake", "synthetic_voice_suspected",
                   "financial_call_to_action", "telegram_contact"],
  "label": "scam", "fraud_type": "deepfake_financial_promo",
  "risk_level": "low", "risk_score": 0,
  "annotator": "student_06", "review_status": "approved"
}
```
`risk_score`/`risk_level` вычисляются downstream risk-движком.

---

## 🔒 Этика и безопасность

- ❌ Реальные публичные лица для генерации **не используются** (обобщённые роли, `.example`-домены).
- ❌ Персональные данные не хранятся (телефоны/кошельки — пусто или маски).
- ✅ Тяжёлое видео в репозиторий **не заливается** — только ссылки/ID/метки.
- ✅ Готовые публичные датасеты — в рамках их лицензий (research-only).
- ✅ Вывод — **risk-сигнал, а не обвинение**. Решение за аналитиком.

---

## ⚠️ Ограничения

- Это **MVP, не production**. Готовые модели не валидированы на настоящих video-deepfake
  (FaceForensics++/DFDC доступны по заявке) — возможны пропуски.
- **NPR** ловит сгенерированные лица, **DFDC** — типовой face-swap. Но **топовый face-swap**
  (напр. DeepTomCruise) по лицу не берут даже SOTA-модели — спасает голос (мультимодальность).
  Для лица нужен файнтюн на FF++/DFDC.
- Аудио-ветка уверенно ловит TTS-синтез, но не валидирована на реальных голос-клонах.
- `lip_sync_anomaly` пока не анализируется (нужен SyncNet).
- Веса **NPR/DFDC** — опциональные, локальные (`vendor/`, в репо не входят); без них ансамбль
  работает на 3 ViT + голосе.

---

## 🔗 Контекст

Учебный проект (хакатон). Это **медиа-слой** (Кейс 9) системы Media Fraud Watch:
поставляет `media_anomalies` для entity/risk-движка и Shadow Graph. Полное архитектурное
описание зоны — в `docs/`.
