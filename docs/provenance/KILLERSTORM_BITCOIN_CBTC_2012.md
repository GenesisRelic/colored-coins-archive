# Provenance record: `killerstorm/bitcoin` `cbtc` branch, September 2012

Status: **VERIFIED HISTORICAL SOURCE ARTIFACT / GENESIS CANDIDATE**

This record documents the surviving Bitcoin-Qt Colored Bitcoin proof-of-concept branch `cbtc` in `killerstorm/bitcoin`. It is an earlier implementation family than the later order-based weak-coloring algorithm and must be preserved as its own historical ruleset.

## Canonical source

- Repository: `https://github.com/killerstorm/bitcoin`
- Historical branch: `cbtc`
- Initial color commit: `e64cafd0b5f2cad8bd86068e8661a53fe4d36bb6`
- Timestamp: `2012-09-04T07:57:07Z`
- Git author/committer: Alex Mizrahi
- Commit message: `colored bitcoin proof-of-concept`
- Parent: `90489ae977eb74f0b7e997c8f67683b2c638c6bd`

The branch currently ends at:

- Tip: `cc062e447f626df3dbe2324c312080a619ebf811`
- Timestamp: `2012-09-07T11:24:06Z`
- Message: `multi-colored wallets`

A merge commit `73b8747a9b4c7305235e776b9bf37d2a204f3e51` dated September 4 joins the proof-of-concept work back with contemporaneous Bitcoin history before the September 7 wallet refinement.

## Primitive coloring model

The September 4 implementation modifies Bitcoin itself rather than adding a separate asset client.

It introduces:

- `COLOR_UNKNOWN = -2`
- `COLOR_MIXED = -1`
- `COLOR_DEFAULT = 0`
- transaction-color persistence in `CTxDB`;
- recursive color calculation through transaction inputs;
- wallet filtering by selected color;
- color computation while connecting blocks.

Unlike the later order-based weak-coloring protocol, the primitive model assigns a color to an **entire transaction**. It does not independently color transaction outputs by ordered value intervals.

When all recursively traced input transactions have the same color, the new transaction inherits that color. If inputs have different colors, the transaction becomes `COLOR_MIXED`.

This historical limitation matches later contemporary discussion in which the author described the old prototype as effectively supporting one color per transaction and contrasted it with the more flexible ordered-output algorithm developed afterward.

## Hard-coded source genesis

The most significant archaeological evidence in the September 4 diff is:

`092ec331582704a05c5c0bde0b70825b2d31aea8342650582d889240da364397`

The implementation's `CTransaction::GetPredefinedColor()` checks the transaction hash and returns color `1` when it matches that value.

Conceptually:

```text
if txid == 092ec331...64397:
    color = 1
elif transaction is coinbase:
    color = uncolored/default
else:
    recursively derive color from input transactions
```

This is stronger evidence than a generic example TXID: the transaction is literally embedded in the historical coloring kernel as the predefined root of color 1.

Current classification:

**SOURCE-VERIFIED GENESIS CANDIDATE**

Not yet established:

- whether the TXID is Bitcoin mainnet, an historical testnet, or testnet3;
- block height and timestamp;
- transaction inputs/outputs and amounts;
- whether the transaction remains available on the relevant chain;
- complete descendant lineage;
- whether any descendant outputs survive unspent.

No claim of a mainnet historical Colored Coin relic should be made until these facts are independently verified.

## September 7 multi-color wallet refinement

Commit `cc062e447f626df3dbe2324c312080a619ebf811`, message `multi-colored wallets`, changes the wallet layer so one wallet can retain transactions of multiple colors while selecting a current color for balances and spendable outputs.

The commit message itself states that:

> Now coins of all colors can be kept in one wallet which would select coins of relevant color when doing queries and operations.

The code stores a color value with wallet transactions and filters balance/available-coin calculations against the selected current color.

The commit timestamp is the same date as the public ChromaWallet proof-of-concept announcement on Bitcointalk.

## Contemporary public link

The surviving ChromaWallet thread eventually documented this branch explicitly as:

`https://github.com/killerstorm/bitcoin/tree/cbtc`

and labeled it the old Bitcoin-Qt proof of concept, noting that it was largely irrelevant after later designs superseded it.

This later labeling is useful because it connects the surviving Git branch to the public Colored Coins development thread rather than leaving the branch as an isolated code artifact.

## Relationship to later protocols

This branch must be modeled separately from:

1. September 27 / October 2012 **order-based weak coloring**, where specific outputs inherit color according to ordered value intervals.
2. October-December 2012 ArmoryX implementation, which uses explicit issue `TXID:vout` definitions.
3. September-October 2013 `vbuterin/coloredcoins` zero-hash marker and metadata-address scheme.
4. EPOBC sequence-tag coloring.
5. Open Assets Protocol.

The `cbtc` branch is a primitive ancestor, not an interchangeable version of those later protocols.

## Archaeological next actions

1. Resolve TXID `092ec331582704a05c5c0bde0b70825b2d31aea8342650582d889240da364397` against historical Bitcoin networks.
2. If found, record block hash/height/time, all inputs, all outputs, script types, values, and spent/unspent state.
3. Reimplement the September 4 transaction-level recursion exactly as a frozen historical kernel.
4. Trace every descendant transaction reachable under those rules.
5. Compare the September 4 candidate lineage with the September 7 wallet behavior.
6. Preserve the complete `cbtc` branch independently as a Git bundle or bare mirror and publish a checksum.
7. Never spend a historical descendant UTXO during verification.
