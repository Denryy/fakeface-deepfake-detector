# FakeFace Findings — Студент 6

> Отчёт по deepfake/video/voice anomaly (Кейс 9). Актуально на текущий срез датасета.

## 1. Что сделано

- Собрано примеров: **75 fake / 75 real** (всего **150**, при минимуме 20 по §15 — перевыполнено).
- Файл с разметкой: `data/processed/deepfake_examples.jsonl` (150 валидных JSONL-строк, 0 битых, 0 дублей).
- Языки: **ru / kk / en** — **каждый речевой сценарий представлен на всех 3 языках** (по 26 речевых строк на язык). Модальности: видео (149) + аудио (1).
- Источники: `data/raw/deepfake/SOURCES.md` (формат `id | origin | url | is_fake | note`).
- Детекторы: `fakeface_detector_stub.py` (черновые `media_anomalies`) + `fakeface_detector_real.py` (реальный видео+аудио, §8).
- Публичные датасеты найдены через **GitHub Search API** (по ТЗ §3.2/§9.3) — храним только ссылки/ID/метки, тяжёлое видео в репозиторий не заливаем (ТЗ §0).

## 2. Источники данных

| origin | fake | real | всего | примечание |
|---|---:|---:|---:|---|
| synthetic | 48 | 6 | 54 | учебные deepfake-промо (инвест/казино/крипта/пирамида/банк) на ru/kk/en, без реальных лиц |
| stock (CC0) | 0 | 37 | 37 | Pexels / Pixabay, real talking heads (ru/kk/en) |
| FaceForensics++ | 10 | 12 | 22 | Deepfakes/Face2Face/FaceSwap/NeuralTextures/FaceShifter + original; research-only |
| FakeAVCeleb | 9 | 9 | 18 | multimodal: FVFA/FVRA/RVFA + RVRA (видео + клон-голос) |
| DFDC | 4 | 7 | 11 | датасет ai.meta.com/datasets/dfdc |
| WildDeepfake | 1 | 4 | 5 | web-collected (OpenTAI/wild-deepfake) |
| DF40 | 2 | 0 | 2 | next-gen deepfake dataset (YZY-stack/DF40) |
| audiofake | 1 | 0 | 1 | синтетический голос (Codecfake) |
| **Итого** | **75** | **75** | **150** | |

Полный перечень сценариев — в §9. Справочные агрегаторы: `Daisy-Zhang/Awesome-Deepfakes-Detection`, `media-sec-lab/Audio-Deepfake-Detection`.

## 3. Метод разметки

Стаб даёт черновые значения, затем — **ручная экспертная проверка каждой строки** по природе источника (ТЗ §5):

- `has_face` — `false` только для audio-only примеров; иначе `true`.
- `possible_deepfake` — `true` для видео-манипуляций (FF++, DFDC, DF40, WildDeepfake, FakeAVCeleb-видео, синтетика); `false` для чисто-аудио фейков.
- `synthetic_voice_suspected` — `true` там, где аудио синтезировано/клонировано (FakeAVCeleb с fake-audio, audiofake, синтетика); `false` для FF++/DFDC/DF40/WildDeepfake (там манипулируется видео, голос реальный).
- `lip_sync_anomaly` — `true` при рассинхроне (FakeAVCeleb FVRA/RVFA/FVFA, синтетика); `false` для видео-свопов без атаки на артикуляцию и для real.

Итоговое распределение сигналов (на 150): `possible_deepfake` — 74, `synthetic_voice_suspected` — 58, `lip_sync_anomaly` — 51, `financial_call_to_action` — 48, `telegram_contact` — 48, `unknown_investment_platform` — 42, `casino_domain_found` — 6. Демо-3 строк (possible_deepfake + financial_call_to_action) — 48.
Синтетическим fake-промо проставлены `transcript`/`ocr_text`/`entities` (домен + Telegram + промокод + финансовый призыв) — для Демо 3 и покрытия не-media сигналов.
Все строки: `review_status = approved`, `annotator = student_06`, поля по схеме §5 (включая `title`/`description`).

## 4. Risk-логика deepfake-кейса

```
possible_deepfake (+25) + financial_call_to_action  → high/critical
+ synthetic_voice_suspected (+25)
+ lip_sync_anomaly (+20)
```
Итоговый `risk_score`/`risk_level` пересчитывает `risk_engine` (Студент 7); в строках оставлены `0`/`low`.

## 5. Интеграция с командой

- Студент 4 (ASR/OCR): беру `transcript` / `ocr_text` для своих видео.
- Студент 7 (entity/risk): отдаю `media_anomalies` + `risk_signals`.
- Студент 8 (граф): узлы `face → video → domain → telegram`.

## 6. Ограничения и риски

- Стаб НЕ является настоящим детектором — решения эвристические/по метке источника + ручная экспертная разметка.
- Доступ к FaceForensics++/DFDC/FakeAVCeleb выдаётся по заявкам/формам — в репозитории только ссылки/ID, не сами клипы.
- `url_or_path` указывает на публичный датасет/репозиторий, а не на конкретный ролик — точный клип выбирается вручную.
- `financial_call_to_action` присутствует у 3 синтетических промо (им добавлены `transcript`/`entities`). Реальные датасетные ролики (FF++/DFDC) не являются финансовой рекламой — финансовый контекст намеренно есть только у синтетических примеров.
- Возможны ложные срабатывания `synthetic_voice_suspected` на эмоциональной речи.
- Реальные публичные лица для генерации не использовались (этика/право, ТЗ §0).
- Вывод системы — только risk-сигнал, не обвинение. Финальное решение — за аналитиком.

## 7. Что улучшить после хакатона

- ✅ Сделано: добавлены `transcript`/`combined_text` (финансовые призывы) к синтетическим fake-промо.
- Подключить реальный детектор (baseline на FaceForensics++).
- Добавить честный lip-sync анализ (SyncNet-подобный).
- Калибровать пороги `risk_score` на размеченной выборке.

## 8. Реальный видео-детектор (эксперимент, бонус)

Помимо стаба реализован **реально работающий** детектор: `src/media/fakeface_detector_real.py`.
В отличие от стаба, он **анализирует сами кадры видео**, а не метку/текст.

Реально анализируются **3 из 4 флагов** (`has_face`, `possible_deepfake`, `synthetic_voice_suspected`).

**Как работает:**
1. OpenCV извлекает ~16 кадров из видео.
2. Haar-каскад детектит лица → `has_face`.
3. Кропы лиц классифицирует предобученная HF-модель `prithivMLmods/Deep-Fake-Detector-Model` (ViT) на GPU (CUDA) → `possible_deepfake` по средней вероятности «Fake».
4. **Аудио-ветка:** ffmpeg извлекает голос (16 кГц моно), модель `motheecreator/Deepfake-audio-detection` (Wav2Vec2) → `synthetic_voice_suspected`.
5. `lip_sync_anomaly` = `false` (нужен SyncNet).

Выход — те же `media_anomalies` (контракт §5), downstream (С7/С8) не меняется.
При сбое зависимостей/модели — автоматический откат на эвристический стаб.

**Видео-ветка** (на CC0 real-видео + GAN-лицо):
- режим важнее модели: одни модели работают по кропу лица, другие — по целому кадру;

| модель | по лицу P(Fake) | по кадру P(Fake) |
|---|---|---|
| prithivMLmods (выбрана) | **0.11 (Real) ✅** | 0.998 ❌ |
| dima806 | 0.99 ❌ | 0.002 ✅ |
| Wvolf | 0.99 ❌ | 0.002 ✅ |

- на реальном видео: `possible_deepfake=false` (P(Fake)=0.28) — ложного срабатывания нет;
- различение real vs GAN-лицо: 0.088 vs 0.257 — в верную сторону (fake выше).

**Аудио-ветка** (работает заметно надёжнее видео-ветки):

| голос | `synthetic_voice_suspected` | P(fake) |
|---|---|---|
| реальный (из видео) | `false` ✅ | 0.000 |
| синтетический gTTS | `true` ✅ | 1.000 |
| синтетический SAPI (pyttsx3) | `true` ✅ | 1.000 |

- проверено end-to-end: ролик `real лицо + синтетический голос` → `synthetic_voice_suspected=true`,
  `possible_deepfake=false` — ровно сценарий Кейса 9 (deepfake-промо с клон-голосом).

**Запуск (через uv):**
```bash
uv venv --system-site-packages
uv pip install -r requirements-detector.txt
.venv/Scripts/python src/media/fakeface_detector_real.py --video path/to/video.mp4
```

**Ограничения (важно):**
- НЕ production-точность. Видео-модель не валидирована на настоящих video-deepfake
  (FaceForensics++/DFDC доступны по заявке) — возможны пропуски (low recall).
- Аудио-ветка уверенно ловит TTS-синтез (gTTS/SAPI), но не валидирована на реальных
  голос-клонах «из дикой природы» — там возможны иные артефакты.
- Чувствительность ограничена: GAN-лицо (0.257) не перешло порог 0.5 — модель обучена
  на face-swap манипуляциях, а не на полностью синтезированных лицах.
- Если в кадрах нет лица — оценка deepfake не выносится (не угадываем по фону).
- `transformers` 5.x несовместим с `torch` 2.6 (нужен `torch.float8_e8m0fnu` из 2.7),
  поэтому детектор живёт в отдельном venv с `transformers==4.49` (см. `requirements-detector.txt`).
- Тяжёлое видео и `.venv/` в git не коммитятся.

## 9. Сценарии датасета (150 примеров)

**Речевые сценарии — каждый на 3 языках (ru / kk / en), по 2 примера на язык (×6).**

**Речевые FAKE (8 архетипов × ru/kk/en × 2 = 48):**

| # | Сценарий | origin | media-флаги |
|---|---|---|---|
| 1 | Предприниматель рекламирует инвест-платформу | synthetic | face+deep+voice+lip |
| 2 | Руководитель банка обещает доход | synthetic | face+deep+voice+lip |
| 3 | Крипто-арбитраж бот «доход без риска» | synthetic | face+deep+voice+lip |
| 4 | Майнинг-инвестиции, пассивный доход | synthetic | face+deep+voice |
| 5 | Блогер рекламирует онлайн-казино (промокод/бонус) | synthetic | face+deep+voice+lip |
| 6 | Финансовый гуру — пирамида (20%/нед, рефералы) | synthetic | face+deep+voice+lip |
| 7 | Розыгрыш призов «от банка» | synthetic | face+deep+voice+lip |
| 8 | Crypto giveaway | synthetic | face+deep+voice+lip |

**Речевые REAL (5 архетипов × ru/kk/en × 2 = 30):**

| # | Сценарий | origin | fraud_type |
|---|---|---|---|
| 1 | Нейтральная говорящая голова | stock | legit_finance |
| 2 | Образование: финансовая безопасность | stock | anti_fraud_education |
| 3 | Запись волонтёра с согласия | synthetic | legit_finance |
| 4 | Интервью эксперта (без призывов) | stock | legit_finance |
| 5 | Легальная реклама банка (без дипфейка) | stock | legit_finance |

**Датасетные указатели (языково-нейтральные — видео-манипуляции, помечены `en`):**
- FAKE (27): FaceForensics++ ×10, FakeAVCeleb FVFA ×9, DFDC ×4, DF40 ×2, WildDeepfake ×1, Codecfake audio ×1.
- REAL (45): stock CC0 ×13, FF++ original ×12, FakeAVCeleb RVRA ×9, DFDC original ×7, WildDeepfake ×4.

> Речевых строк: 78 (по 26 на ru/kk/en). Все сценарии учебные; реальные публичные лица не используются (§0).
> Датасетные примеры — указатели на публичные датасеты (клип выбирается вручную).
