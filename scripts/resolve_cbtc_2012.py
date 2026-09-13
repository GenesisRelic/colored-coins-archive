#!/usr/bin/env python3
"""Resolve and census the September 2012 source-embedded cbtc genesis candidate.

Examples:

  python scripts/resolve_cbtc_2012.py \
      --base-url https://mempool.space \
      --network mainnet

  python scripts/resolve_cbtc_2012.py \
      --base-url https://mempool.space/testnet \
      --network testnet

The script performs GET requests only. It has no transaction broadcast or wallet
capability.
"""

from __future__ import annotations

import argparse
import json

from indexer.cbtc_census import Cbtc2012Census
from indexer.protocols.cbtc_2012 import GENESIS_TXID, RULESET_ID
from indexer.sources.esplora import EsploraError, EsploraSource


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base-url",
        required=True,
        help="Esplora-compatible explorer base URL, e.g. https://mempool.space",
    )
    parser.add_argument(
        "--network",
        required=True,
        help="Evidence label for the queried network, e.g. mainnet or testnet",
    )
    parser.add_argument(
        "--txid",
        default=GENESIS_TXID,
        help="Candidate root TXID; defaults to the September 2012 source anchor",
    )
    parser.add_argument(
        "--no-tx-index",
        action="store_true",
        help="Skip block transaction-index lookup",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    source = EsploraSource(
        args.base_url,
        network_label=args.network,
        resolve_tx_index=not args.no_tx_index,
    )

    try:
        result = Cbtc2012Census(source).scan(args.txid)
    except EsploraError as exc:
        print(
            json.dumps(
                {
                    "ruleset_id": RULESET_ID,
                    "network": args.network,
                    "base_url": args.base_url,
                    "root_txid": args.txid,
                    "status": "lookup-error",
                    "error": str(exc),
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 2

    payload = {
        "ruleset_id": RULESET_ID,
        "network": args.network,
        "base_url": args.base_url,
        "root_txid": result.root_txid,
        "status": "found" if result.root_found else "not-found",
        "surviving_color_sats": result.surviving_color_sats,
        "transactions": [
            {
                "txid": tx.txid,
                "color": tx.color,
                "block_height": tx.block_height,
                "tx_index": tx.tx_index,
                "block_hash": tx.block_hash,
                "block_time": tx.block_time,
            }
            for tx in result.transactions
        ],
        "outputs": [
            {
                "txid": output.txid,
                "vout": output.vout,
                "value_sats": output.value_sats,
                "transaction_color": output.transaction_color,
                "spent_by": output.spent_by,
            }
            for output in result.outputs
        ],
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if result.root_found else 1


if __name__ == "__main__":
    raise SystemExit(main())
