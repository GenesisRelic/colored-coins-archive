"""Frozen reconstruction of the September 2012 `cbtc` coloring rules.

This module models the transaction-level color logic introduced by commit
`e64cafd0b5f2cad8bd86068e8661a53fe4d36bb6` in `killerstorm/bitcoin`.

It is intentionally narrow.  It does not implement later order-based output
coloring, EPOBC, the 2013 marker-address scheme, or Open Assets.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Optional

COLOR_UNKNOWN = -2
COLOR_MIXED = -1
COLOR_DEFAULT = 0
COLOR_ONE = 1

GENESIS_TXID = "092ec331582704a05c5c0bde0b70825b2d31aea8342650582d889240da364397"


@dataclass(frozen=True)
class TxInput:
    """Reference to a parent transaction.

    The historical implementation colored whole transactions, so the parent
    output index is irrelevant to the color calculation itself.  We retain it
    here because a real Bitcoin transaction input identifies a specific
    outpoint and future archaeological tooling will need that provenance.
    """

    txid: str
    vout: int = 0


@dataclass(frozen=True)
class Transaction:
    """Minimal transaction view required by the September 2012 kernel."""

    txid: str
    inputs: tuple[TxInput, ...] = ()
    coinbase: bool = False


ColorResolver = Callable[[str], Optional[int]]


def predefined_color(tx: Transaction) -> int:
    """Return the historical hard-coded color, or ``COLOR_UNKNOWN``.

    The September 4 source hard-coded one transaction hash as color 1 and
    treated coinbase transactions as default/uncolored.
    """

    if tx.txid.lower() == GENESIS_TXID:
        return COLOR_ONE
    if tx.coinbase:
        return COLOR_DEFAULT
    return COLOR_UNKNOWN


def compute_color(tx: Transaction, resolve_parent_color: ColorResolver) -> int:
    """Compute a transaction color using the September 2012 rules.

    Semantics mirror the historical C++ implementation:

    * predefined genesis transaction -> color 1
    * coinbase -> default/uncolored
    * otherwise recurse through parent transactions
    * all known parent colors identical -> that color
    * differing known parent colors -> mixed
    * any unknown parent -> unknown

    ``resolve_parent_color`` should return an integer color constant, or
    ``None`` when the parent cannot be resolved.  ``None`` is normalized to
    ``COLOR_UNKNOWN``.
    """

    color = predefined_color(tx)
    if color != COLOR_UNKNOWN:
        return color

    for txin in tx.inputs:
        parent_color = resolve_parent_color(txin.txid)
        if parent_color is None:
            parent_color = COLOR_UNKNOWN

        if parent_color == COLOR_UNKNOWN:
            return COLOR_UNKNOWN

        if color == COLOR_UNKNOWN:
            color = parent_color
        elif color != parent_color:
            color = COLOR_MIXED

    return color


def compute_color_from_parents(
    txid: str,
    parent_colors: Iterable[int],
    *,
    coinbase: bool = False,
) -> int:
    """Convenience helper for deterministic fixtures and unit tests."""

    colors = tuple(parent_colors)
    tx = Transaction(
        txid=txid,
        inputs=tuple(TxInput(f"parent-{i}") for i in range(len(colors))),
        coinbase=coinbase,
    )
    mapping = {f"parent-{i}": c for i, c in enumerate(colors)}
    return compute_color(tx, mapping.get)
