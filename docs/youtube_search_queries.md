# YouTube Search Queries

> OWNER: Student 1 (YouTube / Shorts). SKELETON.
> Queries below are verbatim from `the project spec §1.3`.

## Queries (spec §1.3)
```text
онлайн казино промокод
казино бонус промокод
слоты промокод
выигрыш казино промокод
депозит бонус казино
вывод денег казино
ставки промокод
казино ссылка в описании
заработок казино
```

## Raw CSV columns (spec §1.3 — contract, see parse_youtube.RAW_CSV_COLUMNS)
```text
source,platform,query,video_id,url,title,description,channel_title,published_at,thumbnail_url
```

## Method (spec §1.3)
- Способ A — YouTube Data API `search.list` (mind quota).
- Способ B — manual: 10–20 public videos; record URL/title/description and what
  is visible on screen (site, promo code, Telegram); 5 synthetic demo clips ok.

## TODO (Student 1)
- [ ] Add KZ-language query variants.
- [ ] Record quota usage.
- [ ] Output rows → `data/processed/youtube_candidates_clean.jsonl` (spec §5).
