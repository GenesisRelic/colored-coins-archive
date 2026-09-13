# Provenance record: `vbuterin/coloredcoins`

Status: **VERIFIED SOURCE ARTIFACT**

This record documents the surviving public GitHub repository `vbuterin/coloredcoins` as an early 2013 Colored Coins implementation artifact. This file is a provenance record only; it does not alter or modernize the historical source.

## Canonical source

- Repository: `https://github.com/vbuterin/coloredcoins`
- Repository owner: `vbuterin`
- Repository name: `coloredcoins`
- Historical/default branch observed during retrieval: `coloredcoins`
- Retrieval date: `2026-09-13`
- Tip commit inspected: `6ae3d0e309543997e427942c72bb1893584ea7fe`
- Tip commit timestamp: `2013-10-06T12:01:37Z`
- Tip commit message: `Added change address to mkgenesis`

The Git commit SHA above is the primary identity for the inspected source state. Future archival snapshots must be verified against this commit rather than against a moving branch name.

## Files at inspected tip

| Path | Git blob SHA |
|---|---|
| `LICENSE` | `370ff710754fbf5ae39fbf727c68a5afc2cdcb6d` |
| `apicli.py` | `9d9361de034582c81856a9969102815cefe57467` |
| `main.js` | `acd8c940482e855b871989611b693c8b801cf566` |
| `package.json` | `c625ba3202d1e7700331ccef426dbfa6c930f7db` |
| `test.js` | `1aa967b3f32a84d7430800252a592b82d45a36c3` |

These blob SHAs provide byte-level Git identities for the five files present at the inspected commit.

## License evidence

The repository's `LICENSE` declares the code public domain and provides an MIT license fallback. The MIT notice states:

- Copyright (c) 2013 Vitalik Buterin
- Permission is granted under the MIT License, subject to preservation of the copyright and permission notice.

The historical license file must be preserved verbatim with any archived source snapshot.

## Protocol observations from the inspected source

These observations are descriptive and must not be confused with a final protocol specification:

1. `package.json` describes the package as `coloredcoins`, version `0.0.8`, with description `Basic colored coins implementation` and author `vbuterin`.
2. `main.js` constructs genesis transactions with colored outputs before a fixed Bitcoin address `1111111111111111111114oLvT2`, followed by metadata outputs.
3. `main.js` contains routines named `find_genesis`, `find_current_owner`, and `get_metadata`, showing that this implementation explicitly attempted to trace a colored unit back to genesis and forward to its current owner.
4. The code uses an order/offset-based flow model across transaction inputs and outputs. Any modern reimplementation must be tested against historical behavior before we label it compatible.

## Preservation rule

No file from the historical repository is to be silently corrected, reformatted, dependency-updated, or security-patched inside the historical archive. Modern fixes belong outside `historical/` and must reference the exact historical commit they reproduce or intentionally diverge from.

## Next archival action

Create an independent immutable snapshot of commit `6ae3d0e309543997e427942c72bb1893584ea7fe`, preserving:

- all original commits reachable from the historical branch,
- commit authors and timestamps,
- tree/blob identities,
- the original license,
- and an independently calculated archive checksum.

A Git bundle or bare mirror is preferred for the long-term archive because it preserves repository history rather than only the working-tree files.
