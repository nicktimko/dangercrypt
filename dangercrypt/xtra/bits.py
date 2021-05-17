"""
Bit manipulation routines
"""
import collections.abc
import enum
import typing


class Bit(enum.IntEnum):
    ZERO = 0
    ONE = 1


class Endian(enum.Enum):
    big = "big"
    little = "little"


def bytes_to_word(
    bytes_: collections.abc.Iterable[int],
    byte_size: int,
    *,
    endian: typing.Union[Endian, str] = Endian.big,
):
    """
    Convert arbitrarly-sized bytes to a word
    """
    endian = Endian(endian)

    if endian is Endian.little:
        bytes_ = reversed(bytes_)

    x = 0
    for n, b in enumerate(bytes_):
        if b >= 1 << byte_size:
            raise ValueError(f"byte {b} at index {n} too wide")
        x <<= byte_size
        x += b

    return x


def byte_to_bits(
    byte: int,
    byte_size: int,
) -> list[int]:
    return [extract_bit(byte, n) for n in range(byte_size)]


def extract_bit(
    byte: int,
    bit: int
) -> Bit:
    return Bit(1 if byte & (1 << bit) else 0)


def iror(byte: int, byte_size: int):
    """Integer Rotate Right"""
    byte, carry = divmod(byte, 2)
    return byte + (carry << (byte_size - 1))


def irol(byte: int, byte_size: int):
    """Integer Rotate Left"""
    carry, byte = divmod(byte << 1, 1 << byte_size)
    return byte + (1 if carry else 0)
