# Provenance record: order-based weak coloring, 2012

Status: **VERIFIED HISTORICAL IMPLEMENTATION LINEAGE**

This record documents the earliest concrete Colored Coins implementation artifacts currently verified in this archive. It deliberately separates evidence, inference, and unresolved questions. It does not claim that any artifact listed here is the first Colored Coins implementation ever made.

## Conceptual precursor

Yoni Assia's surviving article `bitcoin 2.X (aka Colored Bitcoin) - initial specs` carries a March 27, 2012 date and describes a Bitcoin-layer currency created from a genesis transaction, with later balances determined by tracing transaction history back to that genesis. The surviving article credits Lior Hakim for writing the initial specification.

By August 2012, Bitcointalk discussion explicitly used the phrase "coloring bitcoins" for assets on top of Bitcoin without protocol changes. On September 7, 2012 Alex Mizrahi (`killerstorm`) wrote that he had already implemented a simple proof of concept based on tracing coins back to a genesis transaction. That earlier proof-of-concept source has not yet been recovered by this archive.

## Earliest recovered algorithm source in this excavation

A surviving GitHub Gist by `killerstorm`, titled **Coin coloring algorithm demo**, was created September 27, 2012.

- Gist: `https://gist.github.com/killerstorm/3793725`
- File: `colors.cpp`
- Creation date displayed by GitHub: `2012-09-27`

The C++ code assigns logical colors to inputs and consumes input value in transaction order to color outputs. If value from differently colored inputs overlaps the same output, that output becomes mixed. This is the recognizable core of the later order-based weak-coloring implementation.

This September 27 Gist currently predates the standalone repository import described below and is the earliest recovered source artifact for the ordered-value coloring algorithm found in this excavation.

## Standalone `colored-coin-tools` repository

Repository: `https://github.com/killerstorm/colored-coin-tools`

Repository creation: `2012-10-03T10:55:15Z`

Relevant commit lineage:

| Date (UTC) | Commit | Message | Archaeological significance |
|---|---|---|---|
| 2012-10-03 11:01:08 | `7c94cdb8a77cd42e8668dc4b1ac5d663e8964948` | `Initial import of C++ and JS algo demos` | Imports concrete C++ and JavaScript coloring algorithm demos |
| 2012-10-04 07:47:50 | `90b0d5fd2b00f9201b77f16c5495977ce0c0e295` | `moved JS coloring and validation into a separate file,` | Separates the JavaScript coloring/validation kernel |
| 2012-10-30 00:55:54 | `3144c34ab1b35a9d393b4239ecbb68603ae81104` | `added 'the spec' (incomplete)` | Adds written specification for **order-based weak coloring** |
| 2012-11-19 23:18:48 | `275db8e3f48de9e804643d224fefec0652e4c5b1` | `color definition Python code` | Adds programmatic color-definition hashing/validation |
| 2012-11-20 14:43:04 | `2c806005f97c4c031d9e1a7ef1aabe006081364b` | `colordefs web` | Adds web tooling for color definitions |
| 2012-12-01 11:09:39 | `3a365c306193a9224ae232c6cf8a38d7bc2a83f7` | `color definition server` | Adds publication/registry tooling |

The October 30 specification states that a transaction output is colored when it can be traced unambiguously to color-issuing transaction outputs. Inputs and outputs are matched by the overlap of their cumulative value intervals. If all matching inputs are the same color, the output inherits that color; otherwise it becomes uncolored/mixed.

The same specification describes color definitions containing a color identifier, display name, genesis transaction hash, and output index, with optional multiple issuance outputs or an issuing-address mode.

## Armory implementation lineage

The `color` branch of `vbuterin/BitcoinArmory` contains a second implementation lineage built into Bitcoin Armory.

The earliest clearly color-specific commit currently identified in that branch is:

- Commit: `791e3e0d88e15b7d48590f12da8324ebaa5c2854`
- Date: `2012-10-18T10:19:24Z`
- Author: Alex Mizrahi
- Message: `ColorMan, dude`

The commit adds color-management data structures, color issues, ordered input/output coloring, issuance overrides, caches, and sequential blockchain scanning. It descends from ordinary Armory history and therefore provides source-level evidence that Colored Coins functionality was being integrated into a full Bitcoin wallet by October 2012.

This predates the January 2013 transaction-test commit previously used as the earliest Armory anchor in this archive.

## Recovered TESTcc definition

The Armory lineage contains an exact historical default/test color definition tied to:

`c26166c7a387b85eca0adbb86811a9d122a5d96605627ad4125f17f6ddcbf89b:0`

By December 1, 2012 the embedded/default definition contains:

- name: `TESTcc`
- unit: `1`
- style: `genesis`
- issue TXID: `c26166c7a387b85eca0adbb86811a9d122a5d96605627ad4125f17f6ddcbf89b`
- issue output: `0`
- metadata hash: `776d7100a4e22ca75d038d4e533b876f61ecc3a6`
- color ID: `7452b90e22a0b758a048a3db9efa4fd361107350`

The color-definition algorithm independently reproduces these hashes:

1. `HASH160("name:TESTcc:unit:1")` = `776d7100a4e22ca75d038d4e533b876f61ecc3a6`.
2. The resulting canonical definition string, including the issue `TXID:0`, hashes to color ID `7452b90e22a0b758a048a3db9efa4fd361107350`.

This makes TESTcc a deterministic historical test vector for the restoration project.

**Network status remains unresolved.** The presence of this TXID in source does not by itself prove whether the referenced transaction is Bitcoin mainnet, an older testnet, or testnet3. It must be checked against historical chain data before classification.

## Contemporary public ColorID evidence

Contemporary Bitcointalk posts from December 3-8, 2012 describe ArmoryCC/ArmoryX as able to issue colored coins, publish color definitions, and download them by ColorID. The posts give an example asset called **FooCoins** with ColorID:

`c03e572bc2c8520112194a95a29b24c7e99fc87e`

The posts also document the expected local filename:

`~/.armory/colordefs/c03e572bc2c8520112194a95a29b24c7e99fc87e.colordef`

The actual FooCoins definition file has **not** yet been recovered. The historical registry stored generated definitions at runtime and those dynamic files are not present in the surviving `colored-coin-tools` Git tree.

## Historical timeline now supported

The currently verified chronology is therefore:

- **2012-03-27:** surviving Bitcoin 2.X / Colored Bitcoin initial-spec article.
- **2012-08:** public Bitcointalk discussion of coloring Bitcoin as a protocol-layer asset mechanism.
- **2012-09-07:** contemporary claim that a simple tracing proof of concept had already been implemented; source not yet recovered.
- **2012-09-27:** surviving `colors.cpp` order-based coloring Gist.
- **2012-10-03:** standalone C++/JS algorithm repository import.
- **2012-10-18:** color-management implementation integrated into Bitcoin Armory.
- **2012-10-30:** surviving written specification explicitly naming **order-based weak coloring**.
- **2012-11/12:** JSON color definitions, publication tooling, registry, issuance workflow, and public ColorIDs.
- **2013 onward:** later transaction test vectors, exchange experiments, marker-based implementation families, EPOBC, and Open Assets.

## Preservation and interpretation rules

- Do not call the September 27 Gist the "first Colored Coins implementation" without broader evidence.
- Do not infer a transaction's network from source-code context alone.
- Do not conflate order-based weak coloring with the later zero-hash marker implementation, EPOBC, or Open Assets.
- Treat a ColorID as an identifier for a definition, not as the genesis transaction itself.
- Preserve original definitions and source artifacts byte-for-byte when recovered.
- Historical UTXOs are archaeological evidence and must not be moved during reconstruction.

## Priority unresolved targets

1. Recover the pre-September-7 simple proof-of-concept source, if it survives.
2. Recover the exact FooCoins definition for ColorID `c03e572bc2c8520112194a95a29b24c7e99fc87e`.
3. Determine the Bitcoin network and block data for TESTcc issue `c26166c7...:0`.
4. Recover additional 2012 color-definition registry files from archived binaries, mirrors, caches, or historical web archives.
5. Reconstruct all known 2012 issuance definitions into deterministic scanner test vectors.
