"""Minimal read-only Bitcoin transaction model for historical reconstruction."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class TxInput:
    prev_txid: str
    prev_vout: int


@dataclass(frozen=True, slots=True)
class TxOutput:
    value_sats: int
    script_pubkey_hex: str = ""


@dataclass(frozen=True, slots=True)
class TxRecord:
    txid: str
    is_coinbase: bool
    inputs: tuple[TxInput, ...]
    outputs: tuple[TxOutput, ...]
    block_height: int | None = None
    tx_index: int | None = None
    block_hash: str | None = None
    block_time: int | None = None

    def historical_sort_key(self) -> tuple[int, int, str]:
        """Sort confirmed records deterministically by chain position."""

        height = self.block_height if self.block_height is not None else 2**63 - 1
        index = self.tx_index if self.tx_index is not None else 2**63 - 1
        return (height, index, self.txid)


class TransactionSource(Protocol):
    """Read-only transaction source required by archaeology scanners."""

    def get_transaction(self, txid: str) -> TxRecord | None:
        """Return a transaction record or None when unavailable."""

    def get_spender(self, txid: str, vout: int) -> str | None:
        """Return the canonical-chain spender TXID for an output, if any."""
