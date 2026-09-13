"""Read-only descendant census for the September 2012 cbtc ruleset."""

from __future__ import annotations

from dataclasses import dataclass

from indexer.model import TransactionSource, TxRecord
from indexer.protocols.cbtc_2012 import (
    GENESIS_COLOR,
    GENESIS_TXID,
    Color,
    compute_transaction_color,
)


@dataclass(frozen=True, slots=True)
class CensusOutput:
    txid: str
    vout: int
    value_sats: int
    transaction_color: int
    spent_by: str | None


@dataclass(frozen=True, slots=True)
class CensusTransaction:
    txid: str
    color: int
    block_height: int | None
    tx_index: int | None
    block_hash: str | None
    block_time: int | None


@dataclass(frozen=True, slots=True)
class CensusResult:
    root_txid: str
    root_found: bool
    transactions: tuple[CensusTransaction, ...]
    outputs: tuple[CensusOutput, ...]

    @property
    def surviving_color_outputs(self) -> tuple[CensusOutput, ...]:
        return tuple(
            output
            for output in self.outputs
            if output.transaction_color == GENESIS_COLOR and output.spent_by is None
        )

    @property
    def surviving_color_sats(self) -> int:
        return sum(output.value_sats for output in self.surviving_color_outputs)


class Cbtc2012Census:
    """Reconstruct descendants under the primitive whole-transaction rules.

    The scanner follows canonical spenders while a transaction remains color 1.
    A spender that becomes mixed/default/unknown is still included as the
    terminal destruction boundary, but its outputs are not followed further.
    This preserves the first loss-of-color event without wandering indefinitely
    through unrelated later transaction history.
    """

    def __init__(self, source: TransactionSource):
        self.source = source
        self._color_cache: dict[str, int] = {}
        self._classifying: set[str] = set()

    def classify(self, txid: str) -> int:
        """Recursively classify a transaction from its parent transactions."""

        if txid in self._color_cache:
            return self._color_cache[txid]

        tx = self.source.get_transaction(txid)
        if tx is None:
            return int(Color.UNKNOWN)

        if txid in self._classifying:
            raise ValueError(f"transaction graph cycle detected at {txid}")

        self._classifying.add(txid)
        try:
            parent_colors = [self.classify(txin.prev_txid) for txin in tx.inputs]
            color = compute_transaction_color(
                tx.txid,
                is_coinbase=tx.is_coinbase,
                input_colors=parent_colors,
            )
            self._color_cache[txid] = color
            return color
        finally:
            self._classifying.remove(txid)

    def scan(self, root_txid: str = GENESIS_TXID) -> CensusResult:
        """Walk all canonical spend descendants reachable from the root outputs."""

        root = self.source.get_transaction(root_txid)
        if root is None:
            return CensusResult(
                root_txid=root_txid,
                root_found=False,
                transactions=(),
                outputs=(),
            )

        queue = [root_txid]
        seen: set[str] = set()
        records: dict[str, TxRecord] = {}
        outputs: list[CensusOutput] = []

        while queue:
            txid = queue.pop(0)
            if txid in seen:
                continue
            seen.add(txid)

            tx = self.source.get_transaction(txid)
            if tx is None:
                continue

            records[txid] = tx
            color = self.classify(txid)

            for vout, txout in enumerate(tx.outputs):
                spender = self.source.get_spender(txid, vout)
                outputs.append(
                    CensusOutput(
                        txid=txid,
                        vout=vout,
                        value_sats=txout.value_sats,
                        transaction_color=color,
                        spent_by=spender,
                    )
                )
                # Follow a spender only while the source transaction still
                # carries the historical color. A spender of a color-1 output
                # is always inspected, but once that spender classifies as
                # mixed/default/unknown its outputs are recorded as the point
                # where the colored lineage terminates and are not followed
                # further.
                if (
                    color == GENESIS_COLOR
                    and spender is not None
                    and spender not in seen
                ):
                    queue.append(spender)

        ordered_records = sorted(records.values(), key=TxRecord.historical_sort_key)
        transactions = tuple(
            CensusTransaction(
                txid=tx.txid,
                color=self.classify(tx.txid),
                block_height=tx.block_height,
                tx_index=tx.tx_index,
                block_hash=tx.block_hash,
                block_time=tx.block_time,
            )
            for tx in ordered_records
        )

        output_by_tx_position = {
            tx.txid: position for position, tx in enumerate(ordered_records)
        }
        outputs.sort(
            key=lambda output: (
                output_by_tx_position.get(output.txid, 2**63 - 1),
                output.vout,
            )
        )

        return CensusResult(
            root_txid=root_txid,
            root_found=True,
            transactions=transactions,
            outputs=tuple(outputs),
        )
