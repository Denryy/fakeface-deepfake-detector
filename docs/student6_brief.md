# Студент 6 — FakeFace (deepfake / video / voice anomaly)

> Часть проекта **Media Fraud Watch + Shadow Graph**.
> Это твоя рабочая папка. Всё делаешь здесь.

---

## 0. Кто ты в проекте

Ты отвечаешь за **Кейс 9 — Deepfake-реклама** и за поля `media_anomalies` во всём датасете.

Твоя задача — НЕ построить настоящий детектор дипфейков за 24 часа. Твоя задача:

1. Собрать **учебные примеры** real/fake видео (из готовых датасетов + синтетика).
2. Разметить их в едином JSONL-формате с полями аномалий.
3. Сделать **stub-детектор** (`fakeface_detector_stub.py`) — заглушку, которая выдаёт правдоподобные `media_anomalies` по простым эвристикам/метаданным, чтобы demo работало end-to-end.
4. Написать отчёт `fakeface_findings.md`: что собрал, как размечал, какие ограничения.

> **Главная мысль для защиты:** система не утверждает «это дипфейк». Она ставит **risk-сигнал** `possible_deepfake` и объясняет, почему (синтетический голос + финансовый призыв + неизвестная платформа + Telegram). Решение — за аналитиком.

---

## 1. Что ты сдаёшь (Deliverables)

| Файл | Где | Что внутри |
|---|---|---|
| `deepfake_examples.jsonl` | `data/processed/` | ≥ 40 размеченных примеров (20 real + 20 fake), единый JSONL-формат |
| `fakeface_findings.md` | `docs/` | Отчёт: источники, метод, разметка, ограничения |
| `fakeface_detector_stub.py` | `src/media/` | Заглушка-детектор, выдаёт `media_anomalies` |
| Сырьё | `data/raw/deepfake/` | Список ссылок/файлов, `SOURCES.md` (НЕ заливаем тяжёлые видео в git) |

Минимум по спецификации: **20 deepfake/fakeface examples**. Целимся в **40** (20 real / 20 fake), чтобы был баланс классов.

---

## 2. Правила безопасности (ОБЯЗАТЕЛЬНО)

- ❌ НЕ делаем дипфейки реальных публичных людей (политиков, блогеров, знаменитостей).
- ❌ НЕ скачиваем и не распространяем чужие персональные данные.
- ❌ НЕ выносим вывод «человек X — мошенник». Только risk scoring.
- ✅ Используем **готовые публичные датасеты** (FaceForensics++, DFDC, FakeAVCeleb) в рамках их лицензий.
- ✅ Синтетику делаем **без реальных публичных лиц** (свои лица с согласия, нейтральные стоковые/сгенерированные лица, TTS-голоса).
- ✅ В датасете храним только **ссылки/ID/метаданные и наши метки**, не сами тяжёлые видеофайлы в репозитории.

Формулировка результата всегда:
> Система не выносит обвинение. Она выявляет риск-сигналы (`possible_deepfake`, `synthetic_voice_suspected`, `lip_sync_anomaly`), объясняет причины и передаёт материал на ручную проверку аналитика.

---

## 3. Источники данных (твои)

### 3.1. Готовые датасеты (основа)

| Датасет | Что брать | Ссылка | Лицензия / доступ |
|---|---|---|---|
| **FaceForensics++** | примеры real/fake видео (несколько роликов для demo) | https://github.com/ondyari/faceforensics | по запросу формы, research-only |
| **DFDC** (Deepfake Detection Challenge) | маленькая выборка для demo | https://ai.meta.com/datasets/dfdc/ | по согласию с правилами |
| **FakeAVCeleb** | multimodal: видео + клонированный голос | https://github.com/DASH-Lab/FakeAVCeleb | по запросу формы |

> На хакатоне доступ к полным датасетам обычно **не успевают** получить (нужны формы-заявки). Это нормально. План B ниже.

### 3.2. План B — синтетика (если датасеты недоступны)

1. **Real (label=legit/real):** запиши 10–20 коротких роликов сам / с волонтёрами (с согласия), либо возьми CC0-видео «говорящая голова» со стоков (Pexels, Pixabay).
2. **Fake (label=scam/fake):**
   - сгенерируй TTS-озвучку «инвестиционного призыва» (например, любой TTS) — это даёт `synthetic_voice_suspected`;
   - наложи её на видео с несовпадающей артикуляцией → метка `lip_sync_anomaly`;
   - либо опиши «учебный дипфейк-ролик» текстом сценария + метаданными (для demo достаточно).
3. Никаких реальных известных лиц.

### 3.3. Что именно сохраняем из источника

В `data/raw/deepfake/SOURCES.md` для каждого примера:
```
example_id | origin (faceforensics/dfdc/fakeavceleb/synthetic/stock) | url_or_path | is_fake (true/false) | note
```

---

## 4. Конвейер обработки одного примера

```text
Видео (ссылка/файл)
  ↓
[ASR: Whisper] → transcript        (берёшь готовый или сам прогоняешь)
  ↓
[OCR: PaddleOCR] → ocr_text         (текст с кадров: сайт, промокод)
  ↓
fakeface_detector_stub.py
  → media_anomalies:
      has_face
      possible_deepfake
      synthetic_voice_suspected
      lip_sync_anomaly
  ↓
[entity/risk: regex] → entities (url/domain/telegram/promo/wallet/money)
  ↓
risk_signals + risk_score + risk_level
  ↓
строка в deepfake_examples.jsonl
```

Ты не обязан реально гонять Whisper/OCR — это зоны Студента 4. Для своих примеров ты можешь:
- взять их готовые transcript/ocr, **или**
- для синтетики просто вписать текст сценария в `transcript`/`combined_text` вручную.

---

## 5. Поля `media_anomalies` — как ставить

| Поле | true когда | Как определить на MVP |
|---|---|---|
| `has_face` | в кадре есть лицо | глазами / face-detect (OpenCV/face_recognition), или вручную |
| `possible_deepfake` | подозрение на манипуляцию лица/видео | взято из fake-датасета **или** видны артефакты (мерцание краёв лица, неестественная кожа, моргание) |
| `synthetic_voice_suspected` | голос звучит как TTS/клон | монотонность, отсутствие дыхания, ровный темп, метка из FakeAVCeleb |
| `lip_sync_anomaly` | губы не совпадают со звуком | визуальная рассинхронизация |

> Для размеченных fake из датасета `possible_deepfake=true` ставится по факту источника.
> Для real — все поля `false` (кроме `has_face`).

---

## 6. Risk-signals для твоего кейса

Из общего списка тебе релевантны:
```text
possible_deepfake            (+25)
synthetic_voice_suspected    (+25)
lip_sync_anomaly             (+20)
financial_call_to_action
unknown_investment_platform
telegram_contact
casino_domain_found
```

Логика deepfake-кейса:
```text
possible_deepfake + financial_call_to_action  → high / critical
```

Порог risk_score (общий по проекту):
```text
0–24 low | 25–49 medium | 50–79 high | 80–100 critical   (сумма > 100 → 100)
```

---

## 7. Формат строки `deepfake_examples.jsonl`

Одна строка = один JSON (единый формат проекта, секция 5 спецификации). Минимально заполняй:

```json
{
  "id": "deepfake_0001",
  "source": "fakeavceleb / faceforensics / dfdc / synthetic / stock",
  "platform": "youtube / dataset / synthetic",
  "modality": "video",
  "case_type": "deepfake_financial_promo",
  "language": "ru",
  "url": "https://... or local_path",
  "title": "",
  "description": "",
  "transcript": "Я инвестировал в эту платформу, переходите по ссылке...",
  "ocr_text": "invest-example.com @invest_manager",
  "combined_text": "Я инвестировал... invest-example.com @invest_manager",
  "entities": {
    "urls": ["https://invest-example.com"],
    "domains": ["invest-example.com"],
    "telegram_usernames": ["@invest_manager"],
    "phones": [],
    "promo_codes": [],
    "crypto_wallets": [],
    "money_amounts": [],
    "organizations": []
  },
  "media_anomalies": {
    "has_face": true,
    "possible_deepfake": true,
    "synthetic_voice_suspected": true,
    "lip_sync_anomaly": true
  },
  "risk_signals": [
    "possible_deepfake",
    "synthetic_voice_suspected",
    "financial_call_to_action",
    "telegram_contact"
  ],
  "evidence_spans": ["переходите по ссылке", "я инвестировал"],
  "label": "scam",
  "fraud_type": "deepfake_financial_promo",
  "risk_level": "high",
  "risk_score": 75,
  "annotator": "student_06",
  "review_status": "draft"
}
```

Для **real** примера:
```json
{
  "id": "real_0001",
  "source": "stock",
  "modality": "video",
  "case_type": "deepfake_financial_promo",
  "media_anomalies": {"has_face": true, "possible_deepfake": false,
    "synthetic_voice_suspected": false, "lip_sync_anomaly": false},
  "risk_signals": [],
  "label": "legit",
  "fraud_type": "legit_finance",
  "risk_level": "low",
  "risk_score": 0,
  "annotator": "student_06",
  "review_status": "draft"
}
```

> `annotator` всегда `student_06`. `review_status`: `draft` → `approved` после самопроверки.

---

## 8. Пошаговый план (на хакатон)

**Час 0–1. Подготовка**
- [ ] Проверил структуру папки (она уже создана).
- [ ] Подал заявки на FaceForensics++ / FakeAVCeleb (на случай если дадут доступ).
- [ ] Если доступа нет → идём по плану B (синтетика).

**Час 1–4. Сбор сырья**
- [ ] 20 real-роликов (стоки CC0 / свои с согласия) → записал в `SOURCES.md`.
- [ ] 20 fake: синтетика (TTS + рассинхрон) или примеры из датасета.

**Час 4–7. Разметка**
- [ ] Прогнал `fakeface_detector_stub.py` → черновые `media_anomalies`.
- [ ] Вручную проверил и поправил каждое поле.
- [ ] Заполнил `transcript`/`combined_text` (свои или от Студента 4).
- [ ] Получил ≥ 40 строк в `deepfake_examples.jsonl`.

**Час 7–9. Интеграция**
- [ ] Согласовал поля с Студентом 7 (entity/risk) и Студентом 8 (граф).
- [ ] Проверил, что строки валидируются (`python -m json.tool` по каждой).

**Час 9+. Отчёт**
- [ ] Заполнил `docs/fakeface_findings.md`.
- [ ] Подготовил Демо 3 (deepfake financial promo).

---

## 9. Как запустить stub-детектор

```bash
cd /c/Users/Denry/Desktop/fakeface-student6
python src/media/fakeface_detector_stub.py --input data/raw/deepfake/SOURCES.md --out data/processed/deepfake_examples.jsonl
```

Или импортом из своего скрипта:
```python
from src.media.fakeface_detector_stub import analyze_media
anomalies = analyze_media(is_fake_hint=True, transcript="я инвестировал...", has_voice=True)
```

Подробности — в самом файле и в `docs/fakeface_findings.md`.

---

## 10. Demo 3 — твой выход на защите

```text
Загружаем видео
  → FakeFace stub: possible_deepfake = true, synthetic_voice_suspected = true
  → ASR/OCR находит финансовый призыв + сайт + Telegram
  → Entity Agent: domain, telegram_username
  → Risk Engine: possible_deepfake + financial_call_to_action = HIGH/CRITICAL
  → Shadow Graph: face → video → invest_domain → telegram
```

Главный тезис: **объяснимая цепочка**, а не «AI сказал fake».

---

## 11. Чек-лист перед сдачей

- [ ] ≥ 40 строк в `deepfake_examples.jsonl` (баланс real/fake).
- [ ] Каждая строка — валидный JSON, поля по схеме секции 5 спецификации.
- [ ] `media_anomalies` проверены вручную, не только из стаба.
- [ ] `risk_score` согласован с порогами.
- [ ] Нет реальных известных лиц / персональных данных.
- [ ] `fakeface_findings.md` заполнен (источники + ограничения).
- [ ] `review_status` выставлен.
```
