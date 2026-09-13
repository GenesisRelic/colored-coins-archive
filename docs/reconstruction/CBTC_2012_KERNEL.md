# Reconstruction kernel: September 2012 `cbtc`

Status: **IMPLEMENTED / TESTED / TESTNET3 LINEAGE RECONSTRUCTED**

This document defines the first modern reconstruction kernel in the archive. It re-expresses the historical behavior of Alex Mizrahi's September 4, 2012 Bitcoin-Qt Colored Bitcoin proof of concept without modifying or spending Bitcoin.

## Historical source anchor

- repository: `https://github.com/killerstorm/bitcoin`
- branch: `cbtc`
- source commit: `e64cafd0b5f2cad8bd86068e8661a53fe4d36bb6`
- commit message: `colored bitcoin proof-of-concept`
- ruleset ID: `killerstorm-bitcoin-cbtc-2012-09-04`

Modern reconstruction code lives at `indexer/protocols/cbtc_2012.py`. It is not historical source code; it is a small, auditable compatibility kernel derived from the historical semantics.

## Frozen ruleset

Historical sentinel values:

| Meaning | Value |
|---|---:|
| unknown | -2 |
| mixed | -1 |
| default / uncolored | 0 |
| source-embedded genesis color | 1 |

Source-embedded genesis:

`092ec331582704a05c5c0bde0b70825b2d31aea8342650582d889240da364397`

Historical classification behavior:

1. The embedded genesis TXID is color 1.
2. Coinbase transactions are default/uncolored.
3. Other transactions derive one color for the whole transaction from their parent transaction colors.
4. If all parents agree, the child inherits that color.
5. If parent colors disagree, the child is mixed.
6. Unknown ancestry remains unknown until resolvable.

This primitive prototype colors entire transactions, not individual outputs. Output-level color in the modern database is therefore only a projection of the transaction color.

## Reconstruction method

The general kernel contains a direct recursive implementation for test vectors and individual classification. The lineage census uses a more efficient equivalent method specialized to this historical ruleset.

Because the source defines exactly one non-default root, the census propagates **color 1 forward from genesis**:

1. Start with the source-embedded root as proven color 1.
2. Discover canonical-chain transactions spending its outputs.
3. Promote a spender to color 1 only when every parent transaction is already proven color 1.
4. Repeat promotion to a fixed point, allowing independently discovered colored branches to recombine.
5. A reached spender that cannot be promoted has at least one non-color-1 parent and is therefore recorded as a terminal mixed boundary.
6. Stop at that first loss-of-color boundary instead of traversing unrelated later history.

This produces the same color-1 frontier without recursively scanning arbitrary uncolored ancestry back toward coinbase.

## Chain adapters and tests

Read-only transaction abstractions live in:

- `indexer/model.py`
- `indexer/sources/esplora.py`
- `indexer/cbtc_census.py`

The Esplora adapter implements GET operations only. No broadcast endpoint exists in the project.

Deterministic fixtures and tests live in:

- `historical/test-vectors/cbtc_2012.json`
- `tests/test_cbtc_2012.py`
- `tests/test_cbtc_census.py`
- `tests/test_esplora_source.py`

GitHub Actions tests run on Python 3.11 and 3.12.

## Network resolution

Two independent read-only Esplora services were queried.

The source-embedded TXID was:

- **not found** by the queried Blockstream Bitcoin mainnet endpoint;
- **not found** by the queried mempool.space Bitcoin mainnet endpoint;
- **found** by Blockstream on Bitcoin testnet3;
- **found** by mempool.space on Bitcoin testnet3.

Resolved genesis:

- network: `bitcoin-testnet3`
- block: `22926`
- block hash: `0000000022682e00fb0aee8186adc712e71254658cccf7878a3eff9ffb7f74ff`
- block time: `2012-09-03T16:31:19Z`
- transaction index: `1`

Both genesis outputs were already spent.

## Census v0.1 result

Independent census runs through Blockstream and mempool.space agree exactly on the relevant protocol state.

The bounded lineage contains:

- 6 archaeologically relevant transactions;
- 4 color-1 transactions including genesis;
- 2 terminal mixed transactions;
- 2 currently unspent color-1 outputs.

Surviving outputs:

| TXID:vout | Block | Value | Testnet P2PKH |
|---|---:|---:|---|
| `64dfdc0c777c1c100cae33a4ca86033f49f122514c9ef84b6fb7ad517a2595ce:0` | 22928 | 499,950,000 sats | `mnL3t1w673AsaCspJqfWQ3nQRft6FsgLpd` |
| `cc5131c3c70d6905625a8294fc4ef52d2fec568f1351a07089d80f07960d127d:0` | 22940 | 2,500,000,000 sats | `mpeL5d4DfERgjEGN74qgCs8Crz435UDLNi` |

Total surviving protocol state: **2,999,950,000 testnet satoshis = 29.9995 tBTC units**.

This figure is not a price, market capitalization, or economic valuation. It is only the amount of currently unspent testnet3 output value classified as color 1 by the September 2012 prototype rules.

Machine-readable evidence:

- candidate manifest: `historical/candidates/cbtc_2012_genesis_092ec331.json`
- frozen census: `historical/census/cbtc_2012_testnet3_v0.1.json`

## Hard boundary

This ruleset remains independent from all later Colored Coins families. It must not use:

- order-based weak-color output matching;
- ArmoryX color-definition semantics;
- the `1111111111111111111114oLvT2` marker scheme;
- EPOBC `nSequence` tags;
- Open Assets markers or Asset IDs.

Those require separate kernels and separate historical evidence.

## v0.1 completion

The original v0.1 objectives are now met:

- historical kernel deterministic and tested;
- embedded genesis network resolved;
- block and transaction metadata captured;
- lineage reconstructed under the September 4 rules;
- surviving UTXOs recorded without being moved;
- conclusions reproduced independently through two public read-only data sources.

The remaining preservation task for this ruleset is to archive the complete historical `cbtc` Git branch as an immutable mirror or Git bundle with published checksums.

The next primary archaeology target is the **2012 order-based weak-coloring / ArmoryX lineage**, beginning with the recovered TESTcc issuance `c26166c7a387b85eca0adbb86811a9d122a5d96605627ad4125f17f6ddcbf89b:0`.
