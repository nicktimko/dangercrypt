import collections.abc
import enum
import operator
import typing
import warnings


# fmt: off
KNOWN_IRREDUCIBLE_POLYS = [
    # https://oeis.org/A014580
    2, 3, 7, 11, 13, 19, 25, 31, 37, 41, 47, 55, 59, 61, 67, 73, 87, 91, 97,
    103, 109, 115, 117, 131, 137, 143, 145, 157, 167, 171, 185, 191, 193, 203,
    211, 213, 229, 239, 241, 247, 253, 283, 285, 299, 301, 313, 319, 333, 351,
    355, 357, 361, 369, 375
]
# fmt: on


class Endian(enum.Enum):
    big = "big"
    little = "little"


def bytes_to_word(
    bytes_: collections.abc.Iterable[int],
    byte_size: int,
    *,
    endian: typing.Union[Endian, str] = Endian.big,
):
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


def ffadd(a, b):
    return a ^ b


def ffmul(a, b, polynomial=0b1_0001_1011):
    """
    "Russian peasant multiplication"

    Adapted from https://en.wikipedia.org/wiki/Finite_field_arithmetic#C_programming_example
    """
    if (
        polynomial < KNOWN_IRREDUCIBLE_POLYS[-1]
        and polynomial not in KNOWN_IRREDUCIBLE_POLYS
    ):
        warnings.warn("using a known-reducible polynomial")

    p = 0
    while a and b:
        # if b is odd, then add the corresponding a to p (final product = sum of all
        # a's corresponding to odd b's)
        if b & 1:
            p ^= a  # since we're in GF(2^m), addition is an XOR

        # GF modulo: if a >= 128, then it will overflow when shifted left, so reduce
        if a & 0x80:
            # XOR with the primitive polynomial x^8 + x^4 + x^3 + x + 1 (0b1_0001_1011)
            # you can change it but it must be irreducible
            a = (a << 1) ^ polynomial
        else:
            a <<= 1  # equivalent to a * 2

        b >>= 1  # equivalent to b // 2
    return p


def pcadd(a: list[int], b: list[int]):
    return [ffadd(aa, bb) for aa, bb in zip(a, b)]


def pcmul(a: list[int], b: list[int]):
    pass


class FFTerm:
    def __init__(self, value):
        self.value = value

    @classmethod
    def coerce(cls, value):
        if isinstance(value, cls):
            return value
        return cls(value)

    @classmethod
    def _val(cls, x):
        if isinstance(x, cls):
            return x.value
        return x

    def __add__(self, other):
        return FFTerm(ffadd(self.value, self.coerce(other).value))

    def __radd__(self, other):
        return FFTerm(ffadd(self.coerce(other).value, self.value))

    def __sub__(self, other):
        return self.__add__(self, other)

    def __rsub__(self, other):
        return self.__radd__(self, other)

    def __eq__(self, other):
        return self._val(other) == self.value

    def __mul__(self, other):
        pass
