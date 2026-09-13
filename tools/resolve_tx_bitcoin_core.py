#!/usr/bin/env python3
"""Read-only Bitcoin Core transaction resolver for archaeological fixtures.

The script intentionally exposes only read operations.  It never creates,
signs, broadcasts, imports, moves, or spends Bitcoin transactions.

A Bitcoin Core node with the relevant historical chain and, for arbitrary
spent historical transactions, `txindex=1` is normally required.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from typing import Any


ALLOWED_NETWORKS = {"mainnet": [], "testnet3": ["-testnet"]}


def bitcoin_cli(binary: str, network: str, method: str, *params: str) -> Any:
    if network not in ALLOWED_NETWORKS:
        raise ValueError(f"unsupported network: {network}")

    command = [binary, *ALLOWED_NETWORKS[network], method, *params]
    proc = subprocess.run(command, text=True, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "bitcoin-cli failed")

    text = proc.stdout.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def resolve(binary: str, network: str, txid: str) -> dict[str, Any]:
    chain = bitcoin_cli(binary, network, "getblockchaininfo")
    tx = bitcoin_cli(binary, network, "getrawtransaction", txid, "true")

    result: dict[str, Any] = {
        "network_requested": network,
        "chain": chain.get("chain") if isinstance(chain, dict) else None,
        "txid": txid,
        "transaction": tx,
    }

    if isinstance(tx, dict):
        blockhash = tx.get("blockhash")
        if blockhash:
            header = bitcoin_cli(binary, network, "getblockheader", blockhash, "true")
            result["block"] = header
        else:
            result["block"] = None

    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Resolve one historical transaction through a local Bitcoin Core node."
    )
    parser.add_argument("txid", help="64-character transaction ID")
    parser.add_argument(
        "--network",
        choices=sorted(ALLOWED_NETWORKS),
        required=True,
        help="Bitcoin network served by the local node",
    )
    parser.add_argument("--bitcoin-cli", default="bitcoin-cli", help="bitcoin-cli executable")
    args = parser.parse_args()

    if len(args.txid) != 64 or any(c not in "0123456789abcdefABCDEF" for c in args.txid):
        parser.error("txid must be 64 hexadecimal characters")

    try:
        result = resolve(args.bitcoin_cli, args.network, args.txid.lower())
    except Exception as exc:
        print(json.dumps({"resolved": False, "network": args.network, "txid": args.txid.lower(), "error": str(exc)}, indent=2))
        return 2

    print(json.dumps({"resolved": True, **result}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
