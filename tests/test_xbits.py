import pytest

import dangercrypt.xtra.bits as xb


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
    assert xb.bytes_to_word(**i) == o


def test_b2w_oversized():
    with pytest.raises(ValueError, match="too wide"):
        xb.bytes_to_word([0b1000], 3)


@pytest.mark.parametrize(
    "i, o",
    [
        ({"byte": 0b10, "byte_size": 2}, [0, 1]),
        ({"byte": 0b1010, "byte_size": 4}, [0, 1, 0, 1]),
        ({"byte": 0b10101010, "byte_size": 8}, [0, 1, 0, 1, 0, 1, 0, 1]),
        ({"byte": 0b00, "byte_size": 2}, [0, 0]),
        ({"byte": 0, "byte_size": 10}, [0] * 10),
    ]
)
def test_b2bb(i, o):
    assert xb.byte_to_bits(**i) == o


@pytest.mark.parametrize(
    "i, o",
    [
        ({"byte": 0b00, "byte_size": 2}, 0b00),
        ({"byte": 0b01, "byte_size": 2}, 0b10),
        ({"byte": 0b10, "byte_size": 2}, 0b01),
        ({"byte": 0b11, "byte_size": 2}, 0b11),
        ({"byte": 0b1000, "byte_size": 4}, 0b0100),
        ({"byte": 0b0001, "byte_size": 4}, 0b1000),
        ({"byte": 0b00100010, "byte_size": 8}, 0b00010001),
        ({"byte": 0b1, "byte_size": 32}, 0x80000000),
    ]
)
def test_iror(i, o):
    assert xb.iror(**i) == o

@pytest.mark.parametrize(
    "i, o",
    [
        ({"byte": 0b00, "byte_size": 2}, 0b00),
        ({"byte": 0b01, "byte_size": 2}, 0b10),
        ({"byte": 0b10, "byte_size": 2}, 0b01),
        ({"byte": 0b11, "byte_size": 2}, 0b11),
        ({"byte": 0b1000, "byte_size": 4}, 0b0001),
        ({"byte": 0b0001, "byte_size": 4}, 0b0010),
        ({"byte": 0b00100010, "byte_size": 8}, 0b01000100),
        ({"byte": 0b1, "byte_size": 32}, 0b10),
    ]
)
def test_irol(i, o):
    assert xb.irol(**i) == o
