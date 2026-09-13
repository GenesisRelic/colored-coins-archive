#!/usr/bin/env python3
"""Probe one Esplora-compatible network for the September 2012 cbtc root.

This script performs bounded GET-only reconnaissance. It fetches the source-
embedded candidate transaction and, if present, the canonical spender status of
its outputs. It does not recurse through descendants and cannot broadcast.
"""

from __future__ import annotations

import argparse
import json

from indexer.protocols.cbtc_2012 import GENESIS_TXID, RULESET_ID
from indexer.sources.esplora import EsploraError, EsploraSource


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--base-url", required=True)
    p.add_argument("--network", required=True)
    p.add_argument("--txid", default=GENESIS_TXID)
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
            payload = {
                "ruleset_id": RULESET_ID,
                "network": args.network,
                "base_url": args.base_url,
                "root_txid": args.txid,
                "status": "not-found",
            }
            print(json.dumps(payload, indent=2, sort_keys=True))
            return 1

        outputs = []
        for vout, txout in enumerate(tx.outputs):
            outputs.append(
                {
                    "vout": vout,
                    "value_sats": txout.value_sats,
                    "script_pubkey_hex": txout.script_pubkey_hex,
                    "spent_by": source.get_spender(tx.txid, vout),
                }
            )

        payload = {
            "ruleset_id": RULESET_ID,
            "network": args.network,
            "base_url": args.base_url,
            "root_txid": tx.txid,
            "status": "found",
            "is_coinbase": tx.is_coinbase,
            "block_height": tx.block_height,
            "tx_index": tx.tx_index,
            "block_hash": tx.block_hash,
            "block_time": tx.block_time,
            "inputs": [
                {
                    "prev_txid": txin.prev_txid,
                    "prev_vout": txin.prev_vout,
                }
                for txin in tx.inputs
            ],
            "outputs": outputs,
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    except EsploraError as exc:
        payload = {
            "ruleset_id": RULESET_ID,
            "network": args.network,
            "base_url": args.base_url,
            "root_txid": args.txid,
            "status": "lookup-error",
            "error": str(exc),
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
