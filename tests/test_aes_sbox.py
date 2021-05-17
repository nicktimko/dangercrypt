import pytest

from dangercrypt.xtra import bits as xb
from dangercrypt.aes import sbox


@pytest.mark.parametrize(
    "i, o", [
        (0x00, 0x63),
        (0x11, 0x82),
        (0x22, 0x93),
        (0x33, 0xc3),
        (0x30, 0x04),
        (0x52, 0x00),
    ]
)
def test_sbox_basic(i, o):
    assert sbox.sub_byte(i) == xb.byte_to_bits(o, 8)
