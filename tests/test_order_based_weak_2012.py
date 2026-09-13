import unittest

from indexer.protocols.order_based_weak_2012 import (
    COLOR_UNCOLORED,
    COLOR_UNKNOWN,
    InputColor,
    compute_output_colors,
)


class OrderBasedWeak2012Tests(unittest.TestCase):
    def test_historical_red_blue_uncolored_example(self):
        result = compute_output_colors(
            [
                InputColor(1, 1),
                InputColor(2, 1),
                InputColor(1, 2),
                InputColor(4, COLOR_UNCOLORED),
            ],
            [3, 1, 3],
        )
        self.assertTrue(result.valid_value_flow)
        self.assertEqual(result.output_colors, (1, 2, COLOR_UNCOLORED))

    def test_one_colored_input_can_split_across_outputs(self):
        result = compute_output_colors([InputColor(10, 1)], [4, 6])
        self.assertEqual(result.output_colors, (1, 1))

    def test_crossing_color_boundary_destroys_output_color(self):
        result = compute_output_colors(
            [InputColor(5, 1), InputColor(5, 2)],
            [8, 2],
        )
        self.assertEqual(result.output_colors, (COLOR_UNCOLORED, COLOR_UNCOLORED))

    def test_aligned_boundaries_preserve_separate_colors(self):
        result = compute_output_colors(
            [InputColor(5, 1), InputColor(5, 2)],
            [5, 5],
        )
        self.assertEqual(result.output_colors, (1, 2))

    def test_issuance_override_applies_after_normal_coloring(self):
        result = compute_output_colors(
            [InputColor(10, COLOR_UNCOLORED)],
            [10],
            issuance_overrides={0: 7},
        )
        self.assertEqual(result.output_colors, (7,))

    def test_coinbase_stays_uncolored_unless_issued(self):
        normal = compute_output_colors([], [50], is_coinbase=True)
        issued = compute_output_colors(
            [],
            [50],
            is_coinbase=True,
            issuance_overrides={0: 4},
        )
        self.assertEqual(normal.output_colors, (COLOR_UNCOLORED,))
        self.assertEqual(issued.output_colors, (4,))

    def test_invalid_value_flow_leaves_outputs_uncolored_then_overrides_issue(self):
        result = compute_output_colors(
            [InputColor(1, 1)],
            [2, 1],
            issuance_overrides={1: 9},
        )
        self.assertFalse(result.valid_value_flow)
        self.assertEqual(result.output_colors, (COLOR_UNCOLORED, 9))

    def test_zero_valued_output_preserves_historical_unknown_state(self):
        result = compute_output_colors(
            [InputColor(10, 1)],
            [0, 10],
        )
        self.assertEqual(result.output_colors, (COLOR_UNKNOWN, 1))

    def test_negative_amounts_rejected(self):
        with self.assertRaises(ValueError):
            compute_output_colors([InputColor(-1, 1)], [1])
        with self.assertRaises(ValueError):
            compute_output_colors([InputColor(1, 1)], [-1])


if __name__ == "__main__":
    unittest.main()
