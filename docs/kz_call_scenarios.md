# KZ Call Scenarios

> OWNER: Student 5 (KZ calls). SKELETON.
> Scenario stages and keywords are verbatim from
> `the project spec §2`. Real victim recordings are forbidden
> (spec §0, §2.3) — use synthetic scripts (volunteers / TTS) only.

## Stages (spec §2.2, see parse_kz_calls.CALL_STAGES)
1. доставка / eGov → 2. SMS-код → 3. КНБ / полиция / Нацбанк →
4. кредит / угроза → 5. безопасный счёт / перевод.

## Keywords — RU (spec §2.4)
```text
доставка от eGov; код из SMS; код 1414; сотрудник КНБ; сотрудник Нацбанка;
служба безопасности; на вас оформляют кредит; безопасный счёт; не кладите трубку;
никому не говорите; удалённый доступ; AnyDesk; TeamViewer; RustDesk
```

## Keywords — KZ (spec §2.4)
```text
қауіпсіз шот; несие рәсімделді; банк қызметкері; ұлттық банк; SMS кодын айтыңыз;
қосымшаны орнатыңыз; ешкімге айтпаңыз; шұғыл
```

## Method (spec §2.3)
- Способ A — synthetic audio: 30–50 short dialogs from official warnings → TTS /
  volunteers → `.wav` → Whisper → annotate transcript.
- Способ B — text-only: 50 scripts labeled as `text`, add audio later.

## TODO (Student 5)
- [ ] `data/raw/kz_calls/kz_call_scripts.csv`.
- [ ] `data/processed/kz_call_transcripts.jsonl` (spec §5).
