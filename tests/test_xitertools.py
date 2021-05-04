import pytest

import dangercrypt.xtra.itertools as xit


@pytest.mark.parametrize("pad", [xit.NO_PAD, None, "beep"])
def test_pumper_pads(pad):
    it = iter(range(10))

    assert list(xit.pumper(it, 3, pad=pad)) == [0, 1, 2]
    assert list(xit.pumper(it, 3, pad=pad)) == [3, 4, 5]
    assert list(xit.pumper(it, 3, pad=pad)) == [6, 7, 8]

    last = list(xit.pumper(it, 3, pad=pad))
    if pad is xit.NO_PAD:
        assert last == [9]
    else:
        assert last == [9, pad, pad]

    assert list(xit.pumper(it, 3, pad=pad)) == []


@pytest.mark.parametrize(
    "n, raises",
    [
        (0.5, pytest.raises(TypeError, match="integer")),
        ("x", pytest.raises(TypeError, match="integer")),
        (0, pytest.raises(ValueError, match=">= 1")),
    ],
)
def test_pumper_bad_n(n, raises):
    with raises:
        list(xit.pumper([1, 2, 3], n))


def test_chunks():
    assert list(xit.chunks(range(3), 2)) == [[0, 1], [2]]
