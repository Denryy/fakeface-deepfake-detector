# Media Fraud Watch — Студент 6 (FakeFace / deepfake). Архитектура для тимлида

> Документ передачи: что сделано в зоне **Студента 6 (Кейс 9 — deepfake-реклама)**,
> как это устроено и как встраивается в общий конвейер Media Fraud Watch + Shadow Graph.
> Репозиторий зоны: `Desktop/fakeface-student6/`.
> **Опубликован на GitHub:** https://github.com/Denryy/fakeface-deepfake-detector (коммит `6a20692`).
> Примечание: в публичном репо внутренний мастер-ТЗ команды удалён, название проекта и
> упоминания других студентов обезличены — публикуется только зона С6.

---

## 1. Кратко (TL;DR)

Зона Студента 6 — **медиа-слой** системы: определяет признаки подделки лица/голоса в
видео/аудио и выставляет **risk-сигналы** (`possible_deepfake`, `synthetic_voice_suspected`,
`lip_sync_anomaly`). Сама **не выносит вердикт** — отдаёт `media_anomalies` дальше аналитику
и в risk-движок. Главный тезис проекта: *объяснимая цепочка, а не «AI сказал scam»*.

**Готово:**
- ✅ Размеченный датасет: **150 примеров** (75 fake / 75 real), мультиязычный **ru/kk/en**.
  Соответствие схеме §5 перепроверено (150 строк, 0 битых JSON, все поля/типы/enum-ы).
- ✅ Эвристический stub-детектор (для разметки/демо, stdlib-only).
- ✅ **Реальный мультимодальный детектор на GPU** — сверх ТЗ: ансамбль 3 ViT + NPR (generated)
  + DFDC 7×B7 (face-swap) по лицу **и** Wav2Vec2 по голосу.
- ✅ **Веб-UI** для загрузки видео (`detector_server.py`, FastAPI, локально).
- ✅ Отчёт `fakeface_findings.md`, источники `SOURCES.md`.
- ✅ Соответствие ТЗ §5/§6/§7/§9/§13/§14/§15 проверено (аудит).

---

## 2. Артефакты / Deliverables (ТЗ §13/§14)

| Файл | Назначение |
|---|---|
| `data/processed/deepfake_examples.jsonl` | **Итоговый датасет** — 150 строк JSONL по схеме §5 |
| `data/raw/deepfake/SOURCES.md` | Реестр источников (id \| origin \| url \| is_fake \| note) |
| `src/media/fakeface_detector_stub.py` | Эвристический stub-детектор (контракт `media_anomalies`) |
| `src/media/fakeface_detector_real.py` | **Реальный** детектор-ансамбль (видео + аудио, GPU) |
| `src/media/npr_model.py` | NPR (CVPR'24) нашим кодом — сгенерированные лица |
| `src/media/dfdc_model.py` | DFDC EfficientNet-B7 нашим кодом — face-swap |
| `src/media/detector_server.py` | Веб-UI (FastAPI) для загрузки видео |
| `docs/fakeface_findings.md` | Отчёт: источники, метод, сигналы, §8 детектор, §9 сценарии |
| `requirements-detector.txt` | Зависимости реального детектора |
| `pyproject.toml` + `uv.lock` | uv-манифест и lock для воспроизводимой сборки |

> Веса NPR/DFDC (`vendor/`, ~1.8 ГБ) в репозиторий **не входят** (gitignored) — детектор
> работает и без них (просто меньше моделей в ансамбле).

---

## 3. Архитектура зоны (компоненты)

```
┌──────────────────────────── Зона Студента 6 (media) ────────────────────────────┐
│                                                                                   │
│   data/raw/deepfake/SOURCES.md ── реестр источников (real/fake, ссылки/метки)     │
│            │                                                                       │
│            ▼                                                                       │
│   ┌─────────────────────────┐        ┌──────────────────────────────────────┐    │
│   │ fakeface_detector_stub  │        │ fakeface_detector_real (GPU)          │    │
│   │ (эвристика по метке/    │        │  • видео: OpenCV Haar → ViT (лица)    │    │
│   │  тексту, stdlib)        │        │  • аудио: ffmpeg → Wav2Vec2 (голос)   │    │
│   │ → media_anomalies       │        │ → media_anomalies (реальный анализ)   │    │
│   └─────────────────────────┘        └──────────────────────────────────────┘    │
│            │                                   │                                   │
│            └──────────────┬────────────────────┘                                  │
│                           ▼                                                        │
│        data/processed/deepfake_examples.jsonl  (150 размеченных записей §5)        │
└───────────────────────────────────────────────────────────────────────────────────┘
```

- **Два детектора, один контракт.** Оба возвращают одинаковый словарь `media_anomalies`
  (4 поля). Stub нужен для быстрой разметки датасета по метке источника и для demo;
  real — для честного анализа реального видео/аудио.
- **Stub** — без зависимостей (Python stdlib: `argparse`, `json`, `re`).
- **Real** — изолированный uv-venv (см. §7), модели скачиваются с HuggingFace.

---

## 4. Место в общем конвейере (ТЗ §2)

```
Видео / аудио / пост
        │
   [С4] ASR (Whisper) + OCR (PaddleOCR) ─────────► transcript, ocr_text
        │
   [С6] FakeFace detector  ───────────────────────► media_anomalies + media risk_signals
        │                                            (possible_deepfake, synthetic_voice,
        │                                             lip_sync_anomaly)
   [С7] Entity regex + Risk engine ───────────────► entities, risk_score, risk_level
        │
   [С8] Shadow Graph ─────────────────────────────► face → video → domain → telegram
        │
   Analyst Report (explainable)
```

**Студент 6 — поставщик медиа-признаков.** Не считает `risk_score` (это С7), не строит
граф (С8). Отдаёт «сырьё»: размеченные примеры + флаги.

---

## 5. Контракты данных (стабильны — менять только по согласованию)

### 5.1. Запись датасета (ТЗ §5)
Каждая строка `deepfake_examples.jsonl` — один JSON-объект. Обязательные поля:
```
id, source, platform, modality, case_type, language, url, title, description,
transcript, ocr_text, combined_text, entities{8 ключей}, media_anomalies{4 ключа},
risk_signals[], evidence_spans[], label, fraud_type, risk_level, risk_score,
annotator, review_status
```

### 5.2. `media_anomalies` (зона С6 — главный выход)
| Поле | true когда |
|---|---|
| `has_face` | в кадре есть лицо |
| `possible_deepfake` | подозрение на манипуляцию лица/видео |
| `synthetic_voice_suspected` | голос синтезирован/клонирован (TTS) |
| `lip_sync_anomaly` | рассинхрон губ и звука |

### 5.3. Risk-сигналы Кейса 9 (ТЗ §9.4)
`possible_deepfake (+25)`, `synthetic_voice_suspected (+25)`, `lip_sync_anomaly (+20)`,
`financial_call_to_action`, `unknown_investment_platform`, `telegram_contact`, `casino_domain_found`.

### 5.4. Контрактные значения
- `annotator` = `student_06`; `review_status` = `draft` → `approved`.
- `risk_score`/`risk_level` оставлены `0`/`low` — **пересчитывает risk_engine (С7)**.
- Пороги (для С7, §11): `0–24 low | 25–49 medium | 50–79 high | 80–100 critical`.

---

## 6. Детекторы — детали

### 6.1. Stub (`fakeface_detector_stub.py`)
- API: `analyze_media(is_fake_hint, transcript, ...)` → `media_anomalies`;
  `media_risk_signals(anomalies, text)` → список сигналов.
- Решения по метке источника (`is_fake_hint`) + текстовым маркерам.
- CLI: `python src/media/fakeface_detector_stub.py --input SOURCES.md --out deepfake_examples.jsonl`.
- **Важно:** это заглушка для demo/разметки — на произвольном видео без метки даёт «чисто».

### 6.2. Real (`fakeface_detector_real.py`) — мультимодальный АНСАМБЛЬ, 3/4 флага

`possible_deepfake` = **максимум по ансамблю** разнотипных моделей (выше recall):

| Флаг | Как анализируется |
|---|---|
| `has_face` | OpenCV Haar cascade по кадрам |
| `possible_deepfake` | **ансамбль (max):** 3 ViT (`prithivMLmods` по кропу + `dima806`/`Wvolf` по кадру) **+ NPR** (CVPR'24, сгенерированные лица) **+ DFDC** (selimsef, 7×EfficientNet-B7, face-swap) |
| `synthetic_voice_suspected` | ffmpeg извлекает голос → Wav2Vec2 `motheecreator/Deepfake-audio-detection` (GPU) |
| `lip_sync_anomaly` | не анализируется (нужен SyncNet) → `false` |

- NPR/DFDC переписаны **нашим кодом** (timm-энкодер + наш head), веса грузятся безопасно
  (`weights_only=True`); веса локальные (`vendor/`, в репо не входят) → при отсутствии модель
  пропускается. Контракт `media_anomalies` тот же → downstream (С7/С8) не меняется.
- DFDC получает кроп лица с **margin 30%** (как в его обучении); ViT/NPR — плотный кроп.
- Откат на stub при сбое зависимостей/модели.

**Покрытие (проверено на реальных видео):**
| Кейс | Чем ловится |
|---|---|
| Сгенерированное лицо (GAN/diffusion) | ✅ NPR (real 0.006 / GAN 0.996) |
| Типовой face-swap (напр. дипфейк Обамы) | ✅ DFDC / ViT |
| Топовый face-swap (DeepTomCruise) | ⚠️ по лицу OOD для всех (даже DFDC×7 = 0.03) → ловится **голосом** (1.0) |
| Реальное видео | ✅ всё `false` (без ложных срабатываний) |

**Ключевой инсайт:** разные подделки требуют разных детекторов (generated ≠ face-swap),
а топовый face-swap по лицу не берут даже SOTA-модели без файнтюна — **спасает
мультимодальность** (голос). Режим кропа (лицо/кадр) важнее выбора одной модели.

### 6.3. Веб-UI (`detector_server.py`)
Лёгкий FastAPI-сервер: загрузка видео → ансамбль на GPU → флаги `media_anomalies`,
проценты вероятностей, разбивка по моделям, вердикт (фиксированный порог 0.5).
Запуск: `.venv/Scripts/python src/media/detector_server.py` → `http://127.0.0.1:8000`.

---

## 7. Запуск и окружение

### Stub (без зависимостей)
```bash
python src/media/fakeface_detector_stub.py --input data/raw/deepfake/SOURCES.md \
                                           --out data/processed/deepfake_examples.jsonl
```

### Real (GPU) — через uv
```bash
# машина с уже установленным torch cu124 (лёгкая сборка)
uv venv --system-site-packages
uv pip install -r requirements-detector.txt
.venv/Scripts/python src/media/fakeface_detector_real.py --video путь/к/видео.mp4
# --no-audio  чтобы отключить аудио-ветку

# чистая машина (NVIDIA + CUDA 12.4) — self-contained, скачает torch ~2.5ГБ:
#   uv venv && uv pip install ".[gpu]" && uv pip install -r requirements-detector.txt
```

**Окружение проверено:** Windows 11, i5-13420H, 16 GB RAM, **NVIDIA RTX 3050 6GB (CUDA)**,
torch 2.6.0+cu124. Сборка переведена с pip на **uv** (`pyproject.toml` + `uv.lock`).

**⚠️ Подводный камень для команды:** `transformers` 5.x требует `torch ≥ 2.7`
(`torch.float8_e8m0fnu`). С torch 2.6 несовместим → детектор использует
`transformers==4.49` в отдельном uv-venv. `torch` в основные зависимости не включён
(тяжёлый/платформо-зависимый): на машине с torch берётся из системы, на чистой — группа `gpu`.

---

## 8. Датасет (150 примеров)

| Параметр | Значение |
|---|---|
| Всего | **150** (75 fake / 75 real), 0 битых JSON, 0 дублей |
| Языки | **ru / kk / en** — распределены по **уникальным** сценариям (без дублей-переводов; 78/78 речевых строк различны) |
| Источники | synthetic, stock (CC0), FaceForensics++, FakeAVCeleb, DFDC, DF40, WildDeepfake, audio |
| Сценарии | 8 типов речевых fake + 5 типов real — **уникальные записи** (своя формулировка/домен/сумма) + датасетные указатели |
| Демо-3 кейсов | 48 строк (`possible_deepfake` + `financial_call_to_action`) |

**Речевые сценарии fake:** инвест-платформа, банк-CEO, крипто-бот, майнинг, казино,
пирамида, розыгрыш призов, crypto giveaway.
**Речевые real:** нейтральная говорящая голова, финбезопасность (образование), волонтёр,
интервью эксперта, легальная реклама банка.

Полный каталог — `docs/fakeface_findings.md §9`.

**Безопасность (§0):** реальные публичные лица **не используются** (обобщённые роли,
`.example`-домены); тяжёлое видео в репозиторий не заливается — только ссылки/ID/метки;
датасетные примеры — указатели на публичные датасеты.

---

## 9. Точки интеграции (что нужно от/для других)

| С кем | Направление | Контракт |
|---|---|---|
| **С4** (ASR/OCR) | беру | `transcript`, `ocr_text` для своих видео |
| **С7** (entity/risk) | отдаю | `media_anomalies` + media `risk_signals`; С7 считает `risk_score`/`risk_level` |
| **С8** (Shadow Graph) | отдаю | узлы `face → video → domain → telegram` |

**Стыковочный риск:** единого оркестратора (видео→ASR→FakeFace→entity→risk→graph) в
репозитории пока нет — модули есть, «клея» нет. Это общий пробел сборки (ближе к С8/общей
оркестрации), не зоны С6.

---

## 10. Граф знаний проекта

В репозитории есть интерактивный граф знаний (`/understand`): **60 узлов / 91 ребро**,
7 слоёв (Documentation, Data, Ingestion/Parsers, Media Processing, Entity/Risk,
Shadow Graph, App/UI). Файл: `.understand-anything/knowledge-graph.json` (локальный, в git
не коммитится). Запуск дашборда: `/understand-dashboard` (Vite, локально).

> Примечание: помимо зоны С6, в репозитории есть **скаффолд всей командной структуры**
> (§16) — интерфейс-контракты-стабы для С1–С5/С7/С8 (`NotImplementedError` + константы из
> ТЗ). Это архитектурный каркас, не реализация чужих зон.

---

## 11. Статус готовности (чек-лист сдачи, README §11)

| Пункт | Статус |
|---|---|
| ≥40 строк, баланс | ✅ 150 (75/75) |
| Каждая строка — валидный JSON, поля §5 | ✅ 0 ошибок |
| `media_anomalies` проверены вручную | ✅ экспертно по типу источника |
| Нет реальных лиц / перс.данных | ✅ |
| `fakeface_findings.md` заполнен | ✅ |
| `review_status` выставлен | ✅ 150/150 approved |
| `risk_score`/`risk_level` | ⏳ намеренно за С7 (§11) |

**Вывод: зона Студента 6 готова к защите.**

---

## 12. Находка аудита (передать команде)

**Внутреннее расхождение в ТЗ:** сигналы `unknown_investment_platform` (§4.4, §9.4),
`easy_money_claim` (§1.4), `psychological_pressure` (§2.5) используются в кейсах, но
**отсутствуют в «Полном списке» §9**. Затрагивает С1/С2/С4/С7. В нашем контракте
(`signal_extractor.RISK_SIGNALS`) они добавлены с пометкой.

---

## 13. Ограничения и дальнейшие шаги

- Real-детектор — **MVP, не production**. Ансамбль (3 ViT + NPR + DFDC×7) покрывает
  сгенерированные лица и типовой face-swap, но **топовый face-swap** (напр. DeepTomCruise)
  по лицу не берёт **ни одна** готовая модель (даже DFDC×7 ≈ 0.03) — он OOD, сделан после
  публичных датасетов. Такие кейсы ловятся только **голосом** (мультимодальность) или
  **файнтюном** на FaceForensics++/DFDC (доступ по форме — вне хакатона).
- `lip_sync_anomaly` пока не анализируется реально (нужен SyncNet).
- Анализ **содержания** речи (Whisper + текстовые сигналы) — запланирован, не подключён
  (детектор пока чисто медиа: лицо/голос, не «что говорится»).
- Дальше: файнтюн на FF++/DFDC для face-swap, lip-sync (SyncNet), Whisper-ветка,
  единый оркестратор end-to-end.

---

*Контакт по зоне: annotator `student_06`. Все факты в документе подтверждены автотестами
датасета и прогонами детектора на реальном видео.*
