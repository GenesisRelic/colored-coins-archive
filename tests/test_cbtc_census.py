import unittest

from indexer.cbtc_census import Cbtc2012Census
from indexer.model import TxInput, TxOutput, TxRecord
from indexer.protocols.cbtc_2012 import GENESIS_TXID, Color


class MemorySource:
    def __init__(self, transactions, spenders):
        self.transactions = {tx.txid: tx for tx in transactions}
        self.spenders = spenders

    def get_transaction(self, txid):
        return self.transactions.get(txid)

    def get_spender(self, txid, vout):
        return self.spenders.get((txid, vout))


class Cbtc2012CensusTests(unittest.TestCase):
    def setUp(self):
        self.a = "a" * 64
        self.b = "b" * 64
        self.coinbase = "c" * 64
        self.mixed = "d" * 64
        self.mixed_child = "e" * 64

        txs = [
            TxRecord(
                txid=GENESIS_TXID,
                is_coinbase=False,
                inputs=(),
                outputs=(TxOutput(100), TxOutput(50)),
                block_height=100,
                tx_index=1,
            ),
            TxRecord(
                txid=self.coinbase,
                is_coinbase=True,
                inputs=(),
                outputs=(TxOutput(25),),
                block_height=101,
                tx_index=0,
            ),
            TxRecord(
                txid=self.a,
                is_coinbase=False,
                inputs=(TxInput(GENESIS_TXID, 0),),
                outputs=(TxOutput(90),),
                block_height=101,
                tx_index=1,
            ),
            TxRecord(
                txid=self.b,
                is_coinbase=False,
                inputs=(TxInput(GENESIS_TXID, 1),),
                outputs=(TxOutput(40),),
                block_height=102,
                tx_index=0,
            ),
            TxRecord(
                txid=self.mixed,
                is_coinbase=False,
                inputs=(TxInput(self.a, 0), TxInput(self.coinbase, 0)),
                outputs=(TxOutput(110),),
                block_height=103,
                tx_index=0,
            ),
            TxRecord(
                txid=self.mixed_child,
                is_coinbase=False,
                inputs=(TxInput(self.mixed, 0),),
                outputs=(TxOutput(100),),
                block_height=104,
                tx_index=0,
            ),
        ]

        spenders = {
            (GENESIS_TXID, 0): self.a,
            (GENESIS_TXID, 1): self.b,
            (self.a, 0): self.mixed,
            (self.b, 0): None,
            (self.coinbase, 0): self.mixed,
            (self.mixed, 0): self.mixed_child,
            (self.mixed_child, 0): None,
        }
        self.source = MemorySource(txs, spenders)

    def test_recursive_classification(self):
        census = Cbtc2012Census(self.source)
        self.assertEqual(census.classify(GENESIS_TXID), 1)
        self.assertEqual(census.classify(self.a), 1)
        self.assertEqual(census.classify(self.b), 1)
        self.assertEqual(census.classify(self.coinbase), int(Color.DEFAULT))
        self.assertEqual(census.classify(self.mixed), int(Color.MIXED))
        self.assertEqual(census.classify(self.mixed_child), int(Color.MIXED))

    def test_descendant_scan_records_first_mixing_boundary_and_stops(self):
        result = Cbtc2012Census(self.source).scan()

        self.assertTrue(result.root_found)
        self.assertEqual(
            [tx.txid for tx in result.transactions],
            [GENESIS_TXID, self.a, self.b, self.mixed],
        )
        self.assertEqual(
            [tx.color for tx in result.transactions],
            [1, 1, 1, -1],
        )
        self.assertNotIn(
            self.mixed_child,
            [tx.txid for tx in result.transactions],
        )

    def test_surviving_color_supply_counts_only_unspent_color_one_outputs(self):
        result = Cbtc2012Census(self.source).scan()

        self.assertEqual(result.surviving_color_sats, 40)
        self.assertEqual(
            [(o.txid, o.vout, o.value_sats) for o in result.surviving_color_outputs],
            [(self.b, 0, 40)],
        )

    def test_missing_root_is_explicit(self):
        missing_source = MemorySource([], {})
        result = Cbtc2012Census(missing_source).scan()

        self.assertFalse(result.root_found)
        self.assertEqual(result.transactions, ())
        self.assertEqual(result.outputs, ())


if __name__ == "__main__":
    unittest.main()
