import pytest

import dangercrypt.xtra.math as xm


@pytest.mark.parametrize(
    "i, o",
    [
        ({"bytes_": [0], "byte_size": 8}, 0),
        ({"bytes_": [0xFF], "byte_size": 8}, 255),
        ({"bytes_": [0xFF, 0xFE], "byte_size": 8}, 0xFFFE),
        ({"bytes_": [0xFF, 0xFE], "byte_size": 8, "endian": "big"}, 0xFFFE),
        ({"bytes_": [0xFF, 0xFE], "byte_size": 8, "endian": "little"}, 0xFEFF),
        ({"bytes_": [0xA, 0xB], "byte_size": 4, "endian": "big"}, 0xAB),
        ({"bytes_": [0xA, 0xB], "byte_size": 4, "endian": "little"}, 0xBA),
        ({"bytes_": [0b110, 0b101], "byte_size": 3, "endian": "big"}, 0b110101),
    ],
)
def test_b2w(i, o):
    assert xm.bytes_to_word(**i) == o


def test_b2w_oversized():
    with pytest.raises(ValueError, match="too wide"):
        xm.bytes_to_word([0b1000], 3)


def test_ffadd():
    # examples from section 4.1 (though they're the same...)
    assert xm.ffadd(0b01010111, 0b10000011) == 0b11010100
    assert xm.ffadd(0x57, 0x83) == 0xD4

    # from wikipedia
    assert xm.ffadd(0x53, 0xCA) == 0x99


def test_ffterm_add():
    # __add__ homogenous
    a = xm.FFTerm(0x57)
    b = xm.FFTerm(0x83)
    assert a + b == 0xD4

    # __add__ heterogenous
    c = xm.FFTerm(0x53)
    assert c + 0xCA == 0x99

    # __radd__
    d = xm.FFTerm(0xCA)
    assert 0x53 + d == 0x99


def test_ffmul():
    assert xm.ffmul(0x53, 0xCA) == 0x01


def test_pcadd():
    assert xm.pcadd([0, 1, 2, 3], [2, 3, 5, 7]) == [2, 2, 7, 4]
