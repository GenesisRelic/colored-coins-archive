# Preservation Policy

## 1. Historical source is immutable

Any imported historical repository or file is preserved byte-for-byte where possible. Its original Git history, authorship, timestamps, license, tags, and commit hashes must be retained.

## 2. No backdating

The revival will not create commits, releases, tags, contracts, transactions, or records that falsely imply they existed historically.

## 3. Provenance before branding

Claims such as "original", "first", "continuation", "revival", or "same asset" require documentary or cryptographic evidence.

## 4. Protocol continuity is separate from market identity

Colored Coins historically describes Bitcoin-layer asset-coloring protocols and implementations. A modern ERC-20, SPL token, or other newly issued token is not automatically the original Colored Coins system.

## 5. CoinMarketCap identity

A historic CoinMarketCap UCID will only be claimed if an original CMC listing can be independently verified. If no such listing existed, the revival will not fabricate continuity.

## 6. Modern compatibility layer

Modern code may adapt historical behavior to current Bitcoin Core and contemporary libraries, but each deviation must be documented in `COMPATIBILITY.md` and covered by tests.
