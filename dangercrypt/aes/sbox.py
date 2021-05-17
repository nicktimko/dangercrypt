import functools
import operator

from dangercrypt.xtra import bits as xb


c = 0b01100011
shifts = [0, 4, 5, 6, 7]
shifts_int = 0b11110001


# def sub_byte(b: list[int], nb=8):
#     """
#     """
#     if not isinstance(b, list):
#         bits_in = xb.byte_to_bits(b, nb)
#     else:
#         bits_in = b
#     bits_out = [0] * nb
#     for n in range(nb):
#         bits = [bits_in[(n + s) % nb] for s in shifts] + [xb.extract_bit(c, n)]
#         print(bits)
#         bits_out[n] = functools.reduce(operator.xor, bits)
#     return bits_out


def sub_byte(b: list[int], nb=8) -> list[int]:
    pass


# def sub_byte():
#     pass
