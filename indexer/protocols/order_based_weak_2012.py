"""Frozen reconstruction of the December 2012 Armory order-based coloring kernel.

Historical source anchor:
  repository: https://github.com/vbuterin/BitcoinArmory
  branch: color
  commit: 3c3cc413cdcc3190d994f64c3d84c67f6cc6f0d9
  functions: ComputeTxEltColors / ColorMan::computeTxColors

This is modern read-only reconstruction code, not a historical source snapshot.
It models the Armory implementation used alongside JSON color definitions.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence


RULESET_ID = "armory-order-based-weak-coloring-2012-12-01"
SOURCE_REPOSITORY = "https://github.com/vbuterin/BitcoinArmory"
SOURCE_BRANCH = "color"
SOURCE_COMMIT = "3c3cc413cdcc3190d994f64c3d84c67f6cc6f0d9"

COLOR_UNKNOWN = -2
COLOR_UNCOLORED = -1

TESTCC_TXID = "c26166c7a387b85eca0adbb86811a9d122a5d96605627ad4125f17f6ddcbf89b"
TESTCC_VOUT = 0
TESTCC_COLOR_ID = "7452b90e22a0b758a048a3db9efa4fd361107350"
TESTCC_METADATA_HASH = "776d7100a4e22ca75d038d4e533b876f61ecc3a6"


@dataclass(frozen=True, slots=True)
class InputColor:
    amount_sats: int
    color: int


@dataclass(frozen=True, slots=True)
class ColoringResult:
    valid_value_flow: bool
    output_colors: tuple[int, ...]


def compute_output_colors(
    inputs: Sequence[InputColor],
    output_amounts_sats: Sequence[int],
    *,
    is_coinbase: bool = False,
    issuance_overrides: Mapping[int, int] | None = None,
) -> ColoringResult:
    """Reproduce Armory's historical ordered-value output-color calculation.

    Inputs and outputs are consumed in their transaction order. An output
    inherits the current input color when the value interval covering that
    output is supplied by one color. If the interval crosses differently
    colored inputs, the output becomes COLOR_UNCOLORED.

    The historical code initializes outputs as uncolored, skips normal coloring
    for coinbase transactions, then applies explicit issuance overrides by
    TXID:vout. We preserve that ordering exactly.

    Historical behavior for zero-valued outputs is also preserved: a normal
    zero-valued output receives the current color state without consuming value.
    At the beginning of a transaction that state is COLOR_UNKNOWN.
    """

    for item in inputs:
        if item.amount_sats < 0:
            raise ValueError("input amount cannot be negative")
    if any(value < 0 for value in output_amounts_sats):
        raise ValueError("output amount cannot be negative")

    colors = [COLOR_UNCOLORED for _ in output_amounts_sats]
    valid = True

    if not is_coinbase:
        cur_color = COLOR_UNKNOWN
        cur_amount = 0
        input_index = 0

        for output_index, want_amount in enumerate(output_amounts_sats):
            while cur_amount < want_amount and input_index < len(inputs):
                item = inputs[input_index]

                if cur_amount == 0:
                    cur_color = int(item.color)
                elif cur_color != int(item.color):
                    cur_color = COLOR_UNCOLORED

                cur_amount += item.amount_sats
                input_index += 1

            if cur_amount < want_amount:
                valid = False
                break

            colors[output_index] = cur_color
            cur_amount -= want_amount

        if not valid:
            # ColorMan::computeTxColors leaves its initially-uncolored txc
            # untouched when ComputeTxEltColors fails.
            colors = [COLOR_UNCOLORED for _ in output_amounts_sats]

    for index, color in (issuance_overrides or {}).items():
        if index < 0 or index >= len(colors):
            raise IndexError("issuance override output index out of range")
        colors[index] = int(color)

    return ColoringResult(
        valid_value_flow=valid,
        output_colors=tuple(colors),
    )
