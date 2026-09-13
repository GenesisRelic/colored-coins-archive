from coloredcoins.cbtc2012 import (
    COLOR_DEFAULT,
    COLOR_MIXED,
    COLOR_ONE,
    COLOR_UNKNOWN,
    GENESIS_TXID,
    Transaction,
    TxInput,
    compute_color,
    compute_color_from_parents,
)


def test_source_embedded_genesis_is_color_one():
    tx = Transaction(txid=GENESIS_TXID)
    assert compute_color(tx, lambda _: COLOR_UNKNOWN) == COLOR_ONE


def test_coinbase_is_default_color():
    tx = Transaction(txid="00" * 32, coinbase=True)
    assert compute_color(tx, lambda _: COLOR_UNKNOWN) == COLOR_DEFAULT


def test_single_colored_parent_propagates_color():
    assert compute_color_from_parents("11" * 32, [COLOR_ONE]) == COLOR_ONE


def test_same_color_parents_preserve_color():
    assert compute_color_from_parents("22" * 32, [COLOR_ONE, COLOR_ONE]) == COLOR_ONE


def test_different_parent_colors_become_mixed():
    assert compute_color_from_parents("33" * 32, [COLOR_ONE, COLOR_DEFAULT]) == COLOR_MIXED


def test_mixed_stays_mixed_when_more_known_colors_follow():
    assert compute_color_from_parents(
        "44" * 32,
        [COLOR_ONE, COLOR_DEFAULT, COLOR_ONE],
    ) == COLOR_MIXED


def test_unknown_parent_forces_unknown():
    tx = Transaction(txid="55" * 32, inputs=(TxInput("missing"),))
    assert compute_color(tx, lambda _: None) == COLOR_UNKNOWN


def test_empty_non_coinbase_transaction_is_unknown():
    tx = Transaction(txid="66" * 32)
    assert compute_color(tx, lambda _: COLOR_DEFAULT) == COLOR_UNKNOWN
