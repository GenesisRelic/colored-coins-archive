# Reconstruction kernel: September 2012 `cbtc`

Status: **IMPLEMENTED / READ-ONLY / CHAIN RESOLUTION PENDING**

This document defines the first modern reconstruction kernel in the archive. It re-expresses the historical behavior of Alex Mizrahi's September 4, 2012 Bitcoin-Qt Colored Bitcoin proof of concept without modifying or spending Bitcoin.

## Historical source anchor

- repository: `https://github.com/killerstorm/bitcoin`
- branch: `cbtc`
- source commit: `e64cafd0b5f2cad8bd86068e8661a53fe4d36bb6`
- commit message: `colored bitcoin proof-of-concept`

The modern implementation lives at:

`indexer/protocols/cbtc_2012.py`

It is not historical source code. It is a small, auditable compatibility kernel derived from the historical semantics.

## Frozen ruleset

Ruleset ID:

`killerstorm-bitcoin-cbtc-2012-09-04`

Historical sentinel values:

| Meaning | Value |
|---|---:|
| unknown | -2 |
| mixed | -1 |
| default / uncolored | 0 |
| source-embedded genesis color | 1 |

Source-embedded genesis candidate:

`092ec331582704a05c5c0bde0b70825b2d31aea8342650582d889240da364397`

Classification behavior:

1. If the transaction ID equals the source-embedded genesis TXID, classify it as color 1.
2. Otherwise, if the transaction is coinbase, classify it as default/uncolored.
3. Otherwise, begin unknown and inspect parent transaction colors in input order.
4. If any parent is unknown, classification remains unknown.
5. If all known parents have the same color, inherit that color.
6. If known parent colors disagree, classify the transaction as mixed.

The historical prototype colors entire transactions. It does **not** assign independent colors to individual outputs. The modern indexer therefore projects the transaction-level result onto each output only as an explicit database convenience.

## Deterministic test vectors

Machine-readable vectors are stored at:

`historical/test-vectors/cbtc_2012.json`

Unit tests are stored at:

`tests/test_cbtc_2012.py`

They cover:

- source-genesis override;
- coinbase default color;
- single-parent propagation;
- multiple matching parents;
- mixed known colors;
- unknown-parent propagation;
- default-only ancestry;
- mixed-parent ancestry;
- TXID normalization;
- primitive transaction-color projection to outputs.

The kernel has no network, wallet, signing, broadcasting, or spending functionality.

## Archaeological candidate manifest

The hard-coded transaction has a machine-readable candidate record at:

`historical/candidates/cbtc_2012_genesis_092ec331.json`

Its current state is deliberately:

`source-verified-network-unresolved`

No block height, network, outputs, descendants, or surviving UTXOs are asserted yet.

## Chain-resolution stage

The next indexer layer should accept a read-only Bitcoin transaction source and answer, for each candidate TXID:

1. Does the TXID exist on Bitcoin mainnet?
2. Does it exist on the surviving historical test networks available to the data source?
3. What block contains it?
4. What are its inputs, outputs, values, and scripts?
5. Which later transactions spend those outputs?
6. Applying this exact historical kernel recursively, which descendants remain color 1, become mixed, or become unknown?
7. Which candidate-colored outputs remain unspent today?

Public explorers such as mempool.space expose read-only transaction, status, and outspend endpoints for current Bitcoin mainnet and testnet. Those endpoints are useful for spot verification, but the exhaustive census should ultimately use a reproducible local Bitcoin data source so results do not depend on a third-party API.

## Hard boundary

This ruleset must remain independent from all later protocol families.

Do not use:

- order-based weak-color output matching;
- ArmoryX color-definition semantics;
- the `1111111111111111111114oLvT2` marker scheme;
- EPOBC `nSequence` tags;
- Open Assets markers or Asset IDs.

Those require their own kernels and test vectors.

## Definition of success for v0.1

`cbtc-2012 v0.1` is complete when:

- the historical kernel is deterministic and tested;
- the embedded genesis TXID is resolved to a network or conclusively recorded as unavailable in the checked data sources;
- its transaction and block metadata are captured;
- descendants are reconstructed under the September 4 rules;
- current surviving UTXOs, if any, are recorded without being moved;
- every conclusion is reproducible from the archived source and chain data.
