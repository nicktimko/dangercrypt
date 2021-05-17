import pytest

import dangercrypt.xtra.math as xm


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
