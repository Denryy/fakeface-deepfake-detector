# Журнал работы (WORKLOG)

> Что было сделано в репозитории до и включая коммит `deeb410` и обновление графа знаний.
> Файл — мета-документация по сессии, не относится к зоне какого-либо студента.

## 1. Инициализация `CLAUDE.md`
- Проанализирован репозиторий, создан `CLAUDE.md` — руководство для будущих сессий Claude Code.
- Зафиксированы: суть проекта (Студент 6, эвристический stub-детектор, не настоящий ML), главный принцип «risk-сигнал, а не обвинение; решение за аналитиком», команды запуска, поток данных `SOURCES.md → deepfake_examples.jsonl`, и кросс-файловые контракты (`annotator`, `review_status`, пороги `risk_score`).

## 2. Граф знаний (`/understand`) — первая сборка
- Построен `.understand-anything/knowledge-graph.json` по 6 исходным файлам.
- Результат: 12 узлов, 24 ребра, 3 слоя, тур из 6 шагов.
- Запущен интерактивный дашборд (Vite, `http://127.0.0.1:5173`).

## 3. Git: инициализация и первый коммит
- `git init` (ветка `master`), идентичность задана локально.
- `.gitignore`: исключены `.understand-anything/` (локальный кэш графа), тяжёлое медиа (`*.mp4`, `*.wav`…) по правилам безопасности README, Python-мусор.
- Коммит **`8643bc2`** — `chore: initial commit` (код Студента 6 + датасет + доки).
- Включён `autoUpdate: true` в `.understand-anything/config.json`; `meta.json` и `fingerprints.json` привязаны к `8643bc2`.
- Механизм авто-обновления графа: хук плагина срабатывает на **commit** (PostToolUse) и на **старте сессии** при устаревании — но **не на push**.

## 4. Скаффолд архитектуры всей командной репы
По §16 ТЗ сгенерирована структура для всех 8 студенческих пакетов — **только скелеты/контракты, без бизнес-логики, алгоритмов и тестов**. Границы владения сохранены; файлы Студента 6 не тронуты.

- **`src/parsers/`** — `parse_youtube.py` (С1), `parse_telegram_export.py` (С2), `parse_ready_datasets.py` (С3), `parse_kz_calls.py` (С5).
- **`src/media/`** — `asr_whisper.py`, `ocr_paddle.py` (С4); `fakeface_detector_stub.py` (С6) — без изменений.
- **`src/extraction/`** — `regex_extractors.py` (паттерны §10), `signal_extractor.py` (сигналы §9) (С7).
- **`src/risk/risk_engine.py`** — веса §11 + пороги §8 как константы-контракты (С7).
- **`src/graph/`** — `graph_schema.cypher` (схема §12), `build_graph.py` (С8).
- **`src/app/streamlit_app.py`** — UI-каркас (С8).
- **`docs/`** — `annotation_guideline.md`, `dataset_sources.md`, `youtube_search_queries.md`, `kz_call_scenarios.md`, `shadow_graph_demo.md` (скелеты с TODO по студентам).
- **`data/`** — каталоги `raw/*` (`.gitkeep`) + пустые плейсхолдеры `processed/*`.

Контракты спеки вшиты как константы (`PATTERNS`, `RISK_SIGNALS`, `SCORE_WEIGHTS`, `RAW_CSV_COLUMNS`, `CALL_STAGES`); тела функций — `raise NotImplementedError`.

Принятые решения по границам: корневой `README.md` не перезаписан (это бриф Студента 6); `entities_nodes.csv`/`entities_edges.csv` оставлены пустыми (колонки в спеке не заданы — за Студентом 8); общий schema-модуль не добавлялся (нет в §16).

- Коммит **`deeb410`** — `feat: scaffold full team repo architecture (skeletons + contracts)`.

## 5. Граф знаний — пересборка после скаффолда
- Полный пайплайн по **24 значимым файлам** (пустые `__init__.py`, `.gitkeep`, пустые плейсхолдеры исключены).
- Результат: **46 узлов, 74 ребра, 7 слоёв, тур из 11 шагов**. Валидация чистая (0 issues / 0 warnings / 0 orphans).
- **7 слоёв** по пайплайну §13/§16: Documentation & Specification (9) → Data (2) → Ingestion & Parsers (4) → Media Processing (3) → Entity Extraction & Risk Scoring (3) → Shadow Graph (2) → Application & UI (1).
- `meta.json`/`fingerprints.json` перепривязаны к `deeb410` (статус **IN SYNC**).

## Текущее состояние
- Ветка `master`, рабочее дерево чистое; коммиты: `8643bc2`, `deeb410`.
- Граф актуален на `deeb410`. Авто-обновление вооружено (сработает на следующем коммите или старте сессии при устаревании).
