# Provenance record: `vbuterin/BitcoinArmory` color branch

Status: **VERIFIED SOURCE ARTIFACT / TESTNET VECTORS**

This record documents an earlier surviving Colored Coins implementation lineage in the `color` branch of `vbuterin/BitcoinArmory`. It predates the September 2013 `vbuterin/coloredcoins` repository and must be treated as a separate historical ruleset rather than merged with the later marker-address implementation.

## Verified source evidence

- Repository: `https://github.com/vbuterin/BitcoinArmory`
- Historical branch inspected: `color`
- Commit: `92f021b0770cf7504bbe5df17d89044b97fc901b`
- Commit timestamp: `2013-01-27T18:00:20Z`
- Git author/committer metadata: `vub <vub@gmail.com>`
- Commit message: `Changed algorithm to recursive search because a full traversal is needed anyway to rule out mixing, and added more complex test case transactions.`

The commit implements order/value-flow coloring by calculating cumulative input and output values and finding which prior inputs overlap a target output's value interval. It recursively traces all matching parents and treats color mixing as uncolored.

## Historical test vectors

`txcolortest.py` at the historical branch contains explicit transaction hashes with expected color results, including:

- `c1d8d2fb75da30b7b61e109e70599c0187906e7610fe6b12c58eecc3062d1da5:0` — expected `Red`
- `8f6c8751f39357cd42af97a67301127d497597ae699ad0670b4f649bd9e39abf:0` — expected `Red`
- `f50f29906ce306be3fc06df74cc6a4ee151053c2621af8f449b9f62d86cf0647:0` — expected `Blue`
- `7e40d2f414558be60481cbb976e78f2589bc6a9f04f38836c18ed3d10510dce5:0` — expected `Blue`
- `4b60bb49734d6e26d798d685f76a409a5360aeddfddcb48102a7c7ec07243498:0` — expected `Red` after a two-input merge
- `342f119db7f9989f594d0f27e37bb5d652a3093f170de928b9ab7eed410f0bd1:0` — expected uncolored after color mixing
- `bd34141daf5138f62723009666b013e2682ac75a4264f088e75dbd6083fa2dba:0` — expected `Blue` in a complex chain
- `36af9510f65204ec5532ee62d3785584dc42a964013f4d40cfb8b94d27b30aa1:0` — expected `Red` in a complex chain
- `741a53bf925510b67dc0d69f33eb2ad92e0a284a3172d4e82e2a145707935b3e:0` and `:1` — expected `Red` in a complex chain

These are not yet classified as mainnet relics. A contemporaneous Bitcointalk post dated March 9, 2013 explicitly identifies the test server and `txcolortest.py` as operating on **testnet**. The test vectors therefore provide extremely valuable protocol evidence and on-chain testnet archaeology, but must not be presented as historical Bitcoin-mainnet Colored Coin issuance without separate proof.

## Issuance model in the Armory branch

`colortools.py` contains `issue_colored_coins(...)`. The function:

1. selects spendable Bitcoin outputs;
2. creates a recipient output for the requested satoshi amount;
3. optionally creates a change output;
4. signs the transaction;
5. takes the resulting transaction hash;
6. constructs a color definition with `style: genesis` and `issues: [{txhash: <hash>, outindex: 0}]`;
7. finalizes and installs the color definition; and
8. broadcasts the transaction.

This is materially different from the September 2013 `vbuterin/coloredcoins` marker-address scheme. In the Armory lineage, the genesis identity is stored in the color definition as a transaction-output reference; it is not identified by the later zero-hash marker address.

## Color-definition evidence

`colordefs.py` defines color IDs from color-definition data. For `style: genesis`, the color ID commits to the listed issue transaction hashes and output indices. The surviving file also contains example/test genesis definitions referencing transaction output `c26166c7a387b85eca0adbb86811a9d122a5d96605627ad4125f17f6ddcbf89b:0`.

That transaction reference is a **candidate historical test artifact** until its network and role are independently verified from chain data or a contemporary color-definition file.

## Contemporary corroboration

A Bitcointalk bounty thread from February-March 2013 explicitly links Vitalik's `BitcoinArmory` coloring implementation, describes it as working Python code, links the DFS/BFS implementations and `txcolortest.py`, and on March 9 states that the transaction-data server was serving **testnet** and that the test vectors were testnet vectors.

This establishes that the source and transaction hashes were being actively used in the Colored Coins development effort in early 2013, rather than being a later reconstruction.

## Archaeological implication

The archive now has evidence for at least two distinct Vitalik-associated historical implementation families:

1. **Early 2013 Armory order/value-flow coloring** — colors defined by explicit genesis transaction-output references and propagated by ordered value overlap.
2. **September-October 2013 `vbuterin/coloredcoins` marker scheme** — genesis transactions identified structurally by the zero-hash marker address plus ordered outputs and metadata.

A correct historical scanner must not collapse these into one protocol. Each family needs its own rule engine, date range, test vectors, and provenance record.

## Next actions

- Reconstruct the exact Armory color definitions used by the Red/Blue test vectors if surviving copies can be found.
- Verify the listed transaction hashes directly against Bitcoin testnet history.
- Determine whether any equivalent mainnet issues were published using the same Armory rules.
- Preserve the relevant branch/commits independently before relying on upstream availability.
