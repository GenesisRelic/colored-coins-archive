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
        """Reconstruct the color-1 frontier without traversing unrelated ancestry.

        The historical source has exactly one non-default genesis color. That
        lets the census propagate color 1 forward from the source-embedded root
        instead of recursively walking every uncolored parent back to coinbase.

        A spender is promoted to color 1 only when every input parent
        transaction has already been proven color 1. Promotion is repeated to
        a fixed point so transactions combining two independently discovered
        colored branches are handled correctly. Any remaining spender that was
        reached from a color-1 output is therefore a terminal mixed transaction.
        """

        root = self.source.get_transaction(root_txid)
        if root is None:
            return CensusResult(
                root_txid=root_txid,
                root_found=False,
                transactions=(),
                outputs=(),
            )

        records: dict[str, TxRecord] = {root_txid: root}
        colors: dict[str, int] = {root_txid: GENESIS_COLOR}
        pending: dict[str, TxRecord] = {}
        expanded_color1: set[str] = set()

        while True:
            # Discover spenders of every newly proven color-1 transaction.
            expandable = [
                records[txid]
                for txid, color in colors.items()
                if color == GENESIS_COLOR
                and txid in records
                and txid not in expanded_color1
            ]
            expandable.sort(key=TxRecord.historical_sort_key)

            for tx in expandable:
                expanded_color1.add(tx.txid)
                for vout, _txout in enumerate(tx.outputs):
                    spender = self.source.get_spender(tx.txid, vout)
                    if (
                        spender is None
                        or spender in colors
                        or spender in pending
                    ):
                        continue

                    spender_tx = self.source.get_transaction(spender)
                    if spender_tx is None:
                        continue

                    records[spender] = spender_tx
                    pending[spender] = spender_tx

            # Promote candidates whose every parent transaction is already
            # proven color 1. This is exactly the historical all-parents-agree
            # rule specialized to the single source-defined color.
            promoted = [
                txid
                for txid, tx in pending.items()
                if tx.inputs
                and all(
                    colors.get(txin.prev_txid) == GENESIS_COLOR
                    for txin in tx.inputs
                )
            ]

            if promoted:
                for txid in promoted:
                    colors[txid] = GENESIS_COLOR
                    self._color_cache[txid] = GENESIS_COLOR
                    pending.pop(txid)
                continue

            # Fixed point reached. Every remaining candidate was discovered
            # because it spends at least one color-1 output, but at least one
            # of its other parent transactions cannot be proven color 1.
            # Under this 2012 one-genesis ruleset, that makes the transaction
            # mixed and ends the colored lineage at this boundary.
            for txid in pending:
                colors[txid] = int(Color.MIXED)
                self._color_cache[txid] = int(Color.MIXED)
            pending.clear()
            break

        self._color_cache[root_txid] = GENESIS_COLOR

        ordered_records = sorted(records.values(), key=TxRecord.historical_sort_key)
        transactions = tuple(
            CensusTransaction(
                txid=tx.txid,
                color=colors[tx.txid],
                block_height=tx.block_height,
                tx_index=tx.tx_index,
                block_hash=tx.block_hash,
                block_time=tx.block_time,
            )
            for tx in ordered_records
        )

        outputs: list[CensusOutput] = []
        for tx in ordered_records:
            color = colors[tx.txid]
            for vout, txout in enumerate(tx.outputs):
                outputs.append(
                    CensusOutput(
                        txid=tx.txid,
                        vout=vout,
                        value_sats=txout.value_sats,
                        transaction_color=color,
                        spent_by=self.source.get_spender(tx.txid, vout),
                    )
                )

        return CensusResult(
            root_txid=root_txid,
            root_found=True,
            transactions=transactions,
            outputs=tuple(outputs),
        )
