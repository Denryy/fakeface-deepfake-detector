// graph_schema.cypher — Shadow Graph schema (CONTRACT).
//
// OWNER:  Student 8 (Shadow Graph + UI)
// STATUS: SCHEMA CONTRACT — node labels and relationship types are verbatim
//         from the project spec §12. Constraint/index DDL is
//         left as commented placeholders for Student 8 to finalize.
//         No data, no load logic here.
//
// Goal (spec §12.3): surface reuse of the same domain / Telegram / promo code /
// wallet across different videos, posts and sources, and render the cluster
//   blogger -> video -> site -> telegram -> risk_signal.

// --- §12.1 Node labels (CONTRACT — do not rename) ---------------------------
// (:Video) (:Post) (:Call) (:Account) (:Blogger) (:TelegramUsername)
// (:PhoneHash) (:Wallet) (:URL) (:Domain) (:PromoCode) (:Organization)
// (:RiskSignal) (:DatasetSource)

// --- §12.2 Relationship types (CONTRACT — do not rename) --------------------
// (:Blogger)-[:PUBLISHED]->(:Video)
// (:Video)-[:MENTIONS]->(:Domain)
// (:Video)-[:MENTIONS]->(:TelegramUsername)
// (:Video)-[:HAS_PROMO]->(:PromoCode)
// (:Video)-[:HAS_SIGNAL]->(:RiskSignal)
// (:Call)-[:CLAIMS_AUTHORITY]->(:Organization)
// (:Call)-[:REQUESTS]->(:Secret)
// (:Call)-[:HAS_SIGNAL]->(:RiskSignal)
// (:Post)-[:MENTIONS]->(:URL)
// (:URL)-[:HAS_DOMAIN]->(:Domain)
// (:Wallet)-[:REPORTED_IN]->(:ThreatIntel)

// --- Uniqueness constraints (PLACEHOLDER — Student 8 finalizes keys) ---------
// CREATE CONSTRAINT video_id      IF NOT EXISTS FOR (v:Video)            REQUIRE v.id IS UNIQUE;
// CREATE CONSTRAINT domain_name   IF NOT EXISTS FOR (d:Domain)          REQUIRE d.name IS UNIQUE;
// CREATE CONSTRAINT tg_username   IF NOT EXISTS FOR (t:TelegramUsername) REQUIRE t.handle IS UNIQUE;
// CREATE CONSTRAINT promo_code    IF NOT EXISTS FOR (p:PromoCode)       REQUIRE p.code IS UNIQUE;
// CREATE CONSTRAINT wallet_addr   IF NOT EXISTS FOR (w:Wallet)          REQUIRE w.address IS UNIQUE;
