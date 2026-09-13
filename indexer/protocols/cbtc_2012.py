"""Read-only reconstruction of killerstorm's September 2012 cbtc coloring rules.

Historical source:
  repository: https://github.com/killerstorm/bitcoin
  branch: cbtc
  source commit: e64cafd0b5f2cad8bd86068e8661a53fe4d36bb6
  source commit message: "colored bitcoin proof-of-concept"

This module intentionally models the primitive whole-transaction coloring
semantics found in that source. It must not be conflated with later
order-based weak coloring, the 2013 marker-address implementation, EPOBC, or
Open Assets.

The implementation is deliberately side-effect free. It classifies already
known transaction relationships and never broadcasts or spends Bitcoin.
"""

from __future__ import annotations

from enum import IntEnum
from typing import Iterable


RULESET_ID = "killerstorm-bitcoin-cbtc-2012-09-04"
SOURCE_REPOSITORY = "https://github.com/killerstorm/bitcoin"
SOURCE_BRANCH = "cbtc"
SOURCE_COMMIT = "e64cafd0b5f2cad8bd86068e8661a53fe4d36bb6"

GENESIS_TXID = "092ec331582704a05c5c0bde0b70825b2d31aea8342650582d889240da364397"
GENESIS_COLOR = 1


class Color(IntEnum):
    """Historical sentinel values used by the September 2012 implementation."""

    UNKNOWN = -2
    MIXED = -1
    DEFAULT = 0


def normalize_txid(txid: str) -> str:
    """Validate and normalize a conventional 64-character hexadecimal TXID."""

    value = txid.strip().lower()
    if len(value) != 64:
        raise ValueError("txid must contain exactly 64 hexadecimal characters")
    try:
        bytes.fromhex(value)
    except ValueError as exc:
        raise ValueError("txid must be hexadecimal") from exc
    return value


def predefined_color(txid: str, *, is_coinbase: bool) -> int:
    """Return the color fixed by the historical source before parent traversal.

    The September 4 source gives the embedded genesis transaction precedence,
    then treats coinbase transactions as the default/uncolored color. Every
    other transaction begins as COLOR_UNKNOWN and is resolved from its inputs.
    """

    txid = normalize_txid(txid)

    if txid == GENESIS_TXID:
        return GENESIS_COLOR
    if is_coinbase:
        return int(Color.DEFAULT)
    return int(Color.UNKNOWN)


def compute_transaction_color(
    txid: str,
    *,
    is_coinbase: bool,
    input_colors: Iterable[int],
) -> int:
    """Classify one transaction under the September 2012 cbtc rules.

    This follows the behavior of CTransaction::ComputeColor in the historical
    implementation:

    * the hard-coded genesis transaction is color 1;
    * coinbase transactions are default/uncolored;
    * otherwise the transaction inherits a color only when all known parent
      transaction colors agree;
    * encountering an unknown parent leaves the transaction unknown;
    * disagreement between known parent colors yields COLOR_MIXED.

    The historical rules classify whole transactions, not individual outputs.
    """

    color = predefined_color(txid, is_coinbase=is_coinbase)
    if color != int(Color.UNKNOWN):
        return color

    for parent_color in input_colors:
        parent_color = int(parent_color)

        if parent_color == int(Color.UNKNOWN):
            return int(Color.UNKNOWN)

        if color == int(Color.UNKNOWN):
            color = parent_color
        elif color != parent_color:
            color = int(Color.MIXED)

    return color


def all_outputs_share_transaction_color(transaction_color: int, output_count: int) -> tuple[int, ...]:
    """Project the primitive transaction color onto all outputs for indexing.

    The historical cbtc code stores color at transaction level. This helper is
    an explicit modern indexing convenience: every output of that transaction
    receives the same derived transaction color in the archaeological database.
    """

    if output_count < 0:
        raise ValueError("output_count cannot be negative")
    return tuple(int(transaction_color) for _ in range(output_count))
