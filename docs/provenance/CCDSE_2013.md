# Provenance record: CCDSE, January 2013

Status: **VERIFIED HISTORICAL APPLICATION ARTIFACT / ASSET IDENTIFIERS**

This record documents the surviving GitHub artifact for the **Colored Coins Decentralized Stock Exchange (CCDSE)**. It is downstream of the 2012 order-based Colored Coins / ArmoryX work and provides direct evidence that named ColorIDs were being presented as exchange-listed assets in January 2013.

This is an archaeological record. It does not establish that any listed trade occurred, that any asset had legal status, or that any referenced colored outputs survive today.

## Repository

- Surviving repository: `https://github.com/621625/CCDSE`
- Historical project description: `Colored Coins Decentralized Stock Exchange`
- Repository creation: `2013-01-12T06:49:35Z`
- Default branch: `master`
- Surviving history: two commits
- Original links in contemporary posts and page source refer to `github.com/Entrances/CCDSE`; the surviving repository is currently under GitHub account `621625`.

Commits:

| Timestamp (UTC) | Commit | Message |
|---|---|---|
| 2013-01-12 07:16:33 | `822b3418fb2888d9a42078708c0b00b34b2cdc3e` | `Create ccdse.html` |
| 2013-01-12 07:16:56 | `c6a0b193f4cf322125787da0b5761e5f2d9eb9f0` | `Update ccdse.html` |

The final tree contains one file, `ccdse.html`.

## Named historical ColorIDs

The January 12 page presents a "List of assets" and identifies two named colors by ColorID:

### Congo Shares

- Name: `Congo Shares`
- ColorID: `ad0b37e2650341589089c69b870bf47381c08184`

The page also contains a short contract section for Congo Shares and presents numerical listing fields alongside the ColorID. Those numbers are preserved in the source, but this archive does not infer executed trades or historical market value from them.

### Test112

- Name: `Test112`
- ColorID: `1aa66d569297a233d02e79f04cf23cabf58d09f5`

The page presents Test112 in the same asset list.

These are **definition identifiers**, not Bitcoin transaction IDs. To reconstruct the underlying colored genesis outputs, the corresponding historical `.colordef` files must be recovered or independently derived from other primary evidence.

## Contemporary corroboration

On January 12, 2013 a Bitcointalk post announced:

- "Welcome to the colored coins decentralized stock exchange."
- the project was a test;
- a JSBin CCDSE page;
- a Bitcoin forum thread; and
- the GitHub repository then linked as `github.com/Entrances/CCDSE`.

Later the same day, Alex Mizrahi (`killerstorm`) replied that this was, in his words, technically the first colored coin stock exchange, while also recommending that the exchange host color definitions itself because registry availability should not be assumed.

That statement is recorded as a **contemporary participant claim**, not independently promoted here as an absolute historical "first."

## Relationship to ArmoryX

The surviving CCDSE page instructs users to obtain ArmoryX/BitcoinX software and use its color-management interface. This links the application directly to the earlier order-based weak-coloring implementation and ColorID registry workflow.

In that model:

`ColorID -> color definition -> genesis TXID:vout -> order-based colored lineage`

Therefore the recovery of either CCDSE definition file would convert an application-level historical identifier into a specific Bitcoin genesis anchor suitable for deterministic chain reconstruction.

## Priority archaeological targets

1. Recover `ad0b37e2650341589089c69b870bf47381c08184.colordef` for Congo Shares.
2. Recover `1aa66d569297a233d02e79f04cf23cabf58d09f5.colordef` for Test112.
3. Search archived copies of the historical color-definition registry and ArmoryX user directories/binaries.
4. Search old CCDSE mirrors, JSBin revisions, forum attachments, IRC logs, and caches for either ColorID.
5. Once a definition reveals genesis `TXID:vout`, verify its Bitcoin network, block height, amount, descendants, destruction/mixing events, and surviving UTXOs.
6. Do not assign market value or continuity claims until on-chain provenance is established.

## Classification

Current classification:

- CCDSE repository/page: **historically corroborated application artifact**
- Congo Shares ColorID: **historically corroborated asset identifier**
- Test112 ColorID: **historically corroborated asset identifier**
- Underlying genesis transactions: **unresolved**
- Current surviving colored supply: **unresolved**
