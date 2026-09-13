#!/usr/bin/env python3
"""Bounded GET-only probe for one Bitcoin transaction on an Esplora service."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from indexer.sources.esplora import EsploraError, EsploraSource


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--base-url", required=True)
    p.add_argument("--network", required=True)
    p.add_argument("--txid", required=True)
    p.add_argument("--label", default="historical-candidate")
    p.add_argument("--no-tx-index", action="store_true")
    return p


def main() -> int:
    args = parser().parse_args()
    source = EsploraSource(
        args.base_url,
        network_label=args.network,
        resolve_tx_index=not args.no_tx_index,
    )

    try:
        tx = source.get_transaction(args.txid)
        if tx is None:
            print(
                json.dumps(
                    {
                        "label": args.label,
                        "network": args.network,
                        "base_url": args.base_url,
                        "txid": args.txid,
                        "status": "not-found",
                    },
                    indent=2,
                    sort_keys=True,
                )
            )
            return 1

        print(
            json.dumps(
                {
                    "label": args.label,
                    "network": args.network,
                    "base_url": args.base_url,
                    "txid": tx.txid,
                    "status": "found",
                    "is_coinbase": tx.is_coinbase,
                    "block_height": tx.block_height,
                    "tx_index": tx.tx_index,
                    "block_hash": tx.block_hash,
                    "block_time": tx.block_time,
                    "inputs": [
                        {"prev_txid": item.prev_txid, "prev_vout": item.prev_vout}
                        for item in tx.inputs
                    ],
                    "outputs": [
                        {
                            "vout": vout,
                            "value_sats": output.value_sats,
                            "script_pubkey_hex": output.script_pubkey_hex,
                            "spent_by": source.get_spender(tx.txid, vout),
                        }
                        for vout, output in enumerate(tx.outputs)
                    ],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    except EsploraError as exc:
        print(
            json.dumps(
                {
                    "label": args.label,
                    "network": args.network,
                    "base_url": args.base_url,
                    "txid": args.txid,
                    "status": "lookup-error",
                    "error": str(exc),
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
