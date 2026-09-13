# Colored Coins Revival

A historically faithful revival project for early Bitcoin Colored Coins.

## Core principle

This project distinguishes **historical artifacts** from **modern compatibility work**.

Historical source code, specifications, transaction references, hashes, and archived material must be preserved without modification. Modern code lives separately and must document exactly which historical behavior it reproduces or intentionally changes.

## Initial historical anchors

1. Meni Rosenfeld, *Overview of Colored Coins* (December 2012).
2. The early Colored Coins protocol/specification lineage attributed to Meni Rosenfeld, Yoni Assia, Vitalik Buterin and collaborators.
3. `vbuterin/coloredcoins`, a surviving 2013 implementation repository licensed public-domain/MIT.
4. Open Assets Protocol, a later Bitcoin-based Colored Coins implementation/evolution.

## Repository layout

- `historical/` — immutable snapshots and manifests of historical material.
- `docs/` — provenance, protocol history, compatibility and research.
- `src/` — maintained protocol/library code.
- `indexer/` — Bitcoin-chain scanner and color-aware indexer.
- `wallet/` — color-aware wallet tooling.
- `explorer/` — explorer/API layer.
- `tests/` — historical vectors and modern compatibility tests.

See `docs/PRESERVATION_POLICY.md` and `docs/ROADMAP.md`.
