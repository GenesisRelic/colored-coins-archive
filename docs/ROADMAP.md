# Revival Roadmap

## Phase 0 — Provenance

- Freeze authoritative historical sources.
- Record full Git commit hashes, dates, authors and licenses.
- Locate the earliest protocol document versions.
- Reconstruct the claimed first Colored Coins issuance at transaction level.
- Determine whether any original Colored Coins asset had a CoinMarketCap listing/UCID.

## Phase 1 — Reproducibility

- Build a historical development environment for the 2013 implementation.
- Record dependency/runtime assumptions.
- Add fixtures for historical Bitcoin transactions.
- Produce deterministic color-calculation test vectors.

## Phase 2 — Modern indexer

- Connect to modern Bitcoin Core.
- Scan historical Bitcoin blocks and transactions.
- Implement the selected historical coloring rules without changing their semantics.
- Expose an API for color provenance and balances.

## Phase 3 — Wallet and explorer

- Build a watch-only color-aware explorer first.
- Add transaction construction only after parsing/indexing is validated.
- Make ordinary-Bitcoin-spend risks explicit in wallet UX.

## Phase 4 — Public revival

- Publish archival evidence and compatibility report.
- Release signed/tagged binaries or packages.
- Only then evaluate market-data/listing requests, if historically and operationally justified.
