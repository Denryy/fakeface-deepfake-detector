# Dataset Sources

> OWNER: Student 3 (Ready datasets). SKELETON — provenance / licensing notes.
> Source list referenced verbatim from `the project spec §3`.

## Official KZ sources (spec §3.1)
Stop-Piramida.kz (taxonomy & methodology), eGov warnings (scam calls, personal
data), Нацбанк (eGov/КНБ/safe-account scheme; Antifraud-center does not call),
АФМ (bloggers & online casinos).

## Platforms / APIs (spec §3.2)
YouTube Data API `search.list` (+ quota calculator), Whisper (ASR),
PaddleOCR (OCR), PhishTank API (phishing URL checks).

## Ready datasets (spec §3.3)
| Dataset | Use | Access notes |
|---|---|---|
| ScamSpot | financial scam/spam IG comments | public |
| Telegram Spam or Ham | spam/ham baseline | Kaggle |
| ealvaradob/phishing-dataset | phishing/legit URL + HTML | HuggingFace |
| CryptoScamDB | crypto scam URL / addresses | public |
| Chainabuse | public crypto scam reports | public |
| FaceForensics++ / DFDC / FakeAVCeleb | deepfake video/audio | request-form / research-only |

> For each ingested example record provenance in the unified `source` field
> (spec §5) and keep only links/IDs/metadata — never bulk-download heavy media
> into the repo (see `.gitignore`).

## TODO (Student 3)
- [ ] Per-source license/access status table.
- [ ] Counts ingested per source.
- [ ] Mapping notes: raw fields → unified §5 schema.
