# Reproducibility: September 2012 `cbtc` kernel

Status: **INITIAL FROZEN RECONSTRUCTION**

This document defines the first executable reconstruction target for the archive: the transaction-level coloring logic introduced by `killerstorm/bitcoin` commit `e64cafd0b5f2cad8bd86068e8661a53fe4d36bb6` on 2012-09-04.

## Why this kernel comes first

This implementation is earlier and simpler than the later order-based weak-coloring rules. It therefore gives the project a small, deterministic historical kernel that can be verified before full Bitcoin block scanning is introduced.

The reconstruction is intentionally separated from later protocol families. Nothing in this module should silently adopt semantics from ArmoryX, the 2013 zero-hash marker implementation, EPOBC, or Open Assets.

## Frozen historical constants

The reconstruction preserves these logical color values from the historical source:

- `COLOR_UNKNOWN = -2`
- `COLOR_MIXED = -1`
- `COLOR_DEFAULT = 0`
- predefined color `1`

The source-embedded genesis candidate is:

`092ec331582704a05c5c0bde0b70825b2d31aea8342650582d889240da364397`

The historical source returns color `1` for that transaction hash.

## Reconstructed semantics

For one transaction:

1. If the transaction hash equals the embedded genesis candidate, return color `1`.
2. If the transaction is coinbase, return the default/uncolored color.
3. Otherwise resolve each parent transaction color recursively.
4. If any parent color is unknown, return unknown.
5. If all known parent colors agree, inherit that color.
6. If known parent colors differ, return mixed.

This is **transaction-level coloring**. It does not color individual outputs independently.

## Files

- `src/coloredcoins/cbtc2012.py` — frozen pure-Python reconstruction kernel.
- `tests/test_cbtc2012.py` — deterministic semantic tests.
- `fixtures/cbtc2012/genesis_candidate.json` — archaeological fixture for the source-embedded candidate.

The code has no network dependency. That is deliberate: source semantics and chain discovery are separate verification layers.

## Chain-resolution boundary

The fixture currently leaves network, block, transaction hex, outputs, and outspends unset. Public search engines did not surface either this TXID or the later TESTcc TXID during the current investigation, which is insufficient evidence to classify either transaction as absent from Bitcoin mainnet or present on an older test network.

The next chain-verification step must query authoritative chain data directly, preferably a locally controlled Bitcoin Core dataset or multiple independent archival explorers.

A positive match must record at minimum:

- network;
- block height/hash/time;
- raw transaction hex;
- all input outpoints;
- all output values and scripts;
- spent/unspent state of each output;
- descendant transactions under the exact September 2012 recursion rules.

A negative lookup from one explorer is not proof of nonexistence.

## Acceptance criteria for v0.1

The kernel can be considered reproducible when:

- its deterministic tests pass unchanged;
- the historical C++ behavior has been cross-checked line-for-line against the source commit;
- the embedded genesis candidate has been resolved to a specific historical Bitcoin network or explicitly classified as unresolved after archival-node checks;
- a real transaction fixture can be replayed without altering protocol semantics.

## Safety rule

All chain work is read-only. Historical outputs must not be spent, consolidated, swept, or used as test inputs.
