import json
import unittest
from pathlib import Path

from indexer.protocols.cbtc_2012 import (
    GENESIS_TXID,
    Color,
    all_outputs_share_transaction_color,
    compute_transaction_color,
    normalize_txid,
)


FIXTURE = (
    Path(__file__).resolve().parents[1]
    / "historical"
    / "test-vectors"
    / "cbtc_2012.json"
)


class Cbtc2012KernelTests(unittest.TestCase):
    def test_historical_vectors(self):
        data = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.assertEqual(data["genesis_txid"], GENESIS_TXID)

        for vector in data["vectors"]:
            with self.subTest(vector=vector["name"]):
                actual = compute_transaction_color(
                    vector["txid"],
                    is_coinbase=vector["is_coinbase"],
                    input_colors=vector["input_colors"],
                )
                self.assertEqual(actual, vector["expected"])

    def test_non_coinbase_without_resolved_parents_stays_unknown(self):
        txid = "f" * 64
        self.assertEqual(
            compute_transaction_color(
                txid,
                is_coinbase=False,
                input_colors=[],
            ),
            int(Color.UNKNOWN),
        )

    def test_output_projection_keeps_primitive_transaction_color(self):
        self.assertEqual(
            all_outputs_share_transaction_color(1, 3),
            (1, 1, 1),
        )
        self.assertEqual(
            all_outputs_share_transaction_color(int(Color.MIXED), 2),
            (-1, -1),
        )

    def test_output_projection_rejects_negative_count(self):
        with self.assertRaises(ValueError):
            all_outputs_share_transaction_color(1, -1)

    def test_txid_normalization(self):
        self.assertEqual(normalize_txid(GENESIS_TXID.upper()), GENESIS_TXID)

        with self.assertRaises(ValueError):
            normalize_txid("abc")

        with self.assertRaises(ValueError):
            normalize_txid("z" * 64)


if __name__ == "__main__":
    unittest.main()
