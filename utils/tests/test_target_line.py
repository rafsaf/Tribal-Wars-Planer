import pytest

from utils.basic.target_line import LineError, TargetsOneLine


def test_targets_one_line_accepts_default_deff_suffix() -> None:
    coord, line = TargetsOneLine("500|499:2:4+deff").validate_line()

    assert coord == "500|499"
    assert line == "500|499:2:4+4deff"


def test_targets_one_line_defaults_deff_suffix_to_last_noble_wave() -> None:
    _, line = TargetsOneLine("205|205:2:2+deff").validate_line()

    assert line == "205|205:2:2+2deff"


def test_targets_one_line_accepts_explicit_deff_suffix() -> None:
    _, line = TargetsOneLine("500|499:2:5+5deff").validate_line()

    assert line == "500|499:2:5+5deff"


def test_targets_one_line_accepts_extended_noble_deff_suffix() -> None:
    _, line = TargetsOneLine("500|499:2|0|0|0:1|1|1|1+4deff").validate_line()

    assert line == "500|499:2|0|0|0:1|1|1|1+4deff"


@pytest.mark.parametrize(
    "line",
    [
        "500|499:2:4+5deff",
        "500|499:2:4+xdeff",
        "500|499:2:4+0deff",
        "500|499:2:4+deff5",
        "500|499:2:0+deff",
    ],
)
def test_targets_one_line_rejects_invalid_deff_suffix(line: str) -> None:
    with pytest.raises(LineError):
        TargetsOneLine(line).validate_line()
