import itertools
import operator
import random
import re

import pytest

import finite

from tests.util import int_sampler


SMALL_FIELDS = [2, 3, 4, 5, 7, 8, 9, 11, 13, 16, 17, 19, 23, 25, 27]
BIGGER_FIELDS = [256, 10007, 65536, 100003]

MAX_ITER_N = 5000
MAX_ITER_N2 = int(MAX_ITER_N ** (1 / 2))
MAX_ITER_N3 = int(MAX_ITER_N ** (1 / 3))


@pytest.mark.parametrize(
    "n, ex_prime, ex_pow",
    [
        (2, 2, 1),
        (3, 3, 1),
        (4, 2, 2),
        (5, 5, 1),
        (7, 7, 1),
        (8, 2, 3),
        (9, 3, 2),
        (16, 2, 4),
    ],
)
def test_field_creation(n, ex_prime, ex_pow):
    f = finite.Field(n)
    assert f.prime == ex_prime
    assert f.power == ex_pow


def test_superscripts():
    assert (
        finite.int2sup("123")
        == "¹²³"
        == "\N{SUPERSCRIPT ONE}\N{SUPERSCRIPT TWO}\N{SUPERSCRIPT THREE}"
    )


@pytest.mark.parametrize(
    "n, factorization",
    [
        (6, "2 * 3"),
        (10, "2 * 5"),
        (12, "2² * 3"),
        (5040, "2⁴ * 3² * 5 * 7"),
    ],
)
def test_invalid_fields(n, factorization):
    with pytest.raises(ValueError, match=re.escape(factorization)):
        finite.Field(n)


def test_element_generation():
    f = finite.Field(17)
    el = f.element(10)
    assert el.coeff == [10]

    f = finite.Field(16)
    el = f.element(10)
    assert el.coeff == [0, 1, 0, 1]

    f = finite.Field(9)
    el = f.element(7)
    assert el.coeff == [1, 2]


@pytest.mark.parametrize("n", SMALL_FIELDS + BIGGER_FIELDS)
def test_element_roundtrip(n):
    f = finite.Field(n)
    for m in int_sampler(n):
        el = f.element(m)
        assert int(el) == m


@pytest.mark.parametrize("n", SMALL_FIELDS + BIGGER_FIELDS)
def test_characteristic(n):
    f = finite.Field(n)
    _sanity_run_check = False
    for m in int_sampler(n, limit=int(MAX_ITER_N / f.prime) + 1):
        _sanity_run_check = True
        el = f.element(m)
        assert sum(el for _ in range(f.prime)) == f.element(0)
    assert _sanity_run_check


@pytest.mark.parametrize("n", SMALL_FIELDS + BIGGER_FIELDS)
@pytest.mark.parametrize("func", [operator.add, operator.sub])
def test_add_identity(n, func):
    f = finite.Field(n)
    additive_identity = f.element(0)
    for m in int_sampler(n):
        el = f.element(m)
        assert func(el, additive_identity) == el


@pytest.mark.parametrize("n", SMALL_FIELDS + BIGGER_FIELDS)
def test_add_inverse(n):
    f = finite.Field(n)
    additive_identity = f.element(0)
    for m in int_sampler(n):
        el = f.element(m)
        assert el + (-el) == additive_identity


@pytest.mark.parametrize("func", [operator.add, operator.mul])
@pytest.mark.parametrize("n", SMALL_FIELDS)
def test_commutative(n, func):
    f = finite.Field(n)
    for na, nb in int_sampler([n, n]):
        a = f.element(na)
        b = f.element(nb)
        assert func(a, b) == func(b, a), (a, b)


@pytest.mark.parametrize("func", [operator.add, operator.mul])
@pytest.mark.parametrize("n", SMALL_FIELDS)
def test_associative(n, func):
    f = finite.Field(n)
    _op = "*" if func is operator.mul else "+"

    for na, nb, nc in int_sampler([n, n, n], seed=n):
        a = f.element(na)
        b = f.element(nb)
        c = f.element(nc)
        if func(func(a, b), c) != func(a, func(b, c)):
            print(na, nb, nc)
            ab = func(a, b)
            bc = func(b, c)
            ab_c = func(ab, c)
            a_bc = func(a, bc)
            print(f)
            print(f.mod_poly)
            print(f"a: {na} -> {a}")
            print(f"b: {nb} -> {b}")
            print(f"c: {nc} -> {c}")
            print(f"{ab=}, {ab_c=}")
            print(f"{bc=}, {a_bc=}")
            _note = f"in {f}: ({na} {_op} {nb}) {_op} {nc} != {na} {_op} ({nb} {_op} {nc})"
            pytest.fail(_note)


@pytest.mark.parametrize("n", SMALL_FIELDS + BIGGER_FIELDS)
def test_sub(n):
    f = finite.Field(n)
    additive_identity = f.element(0)
    for m in range(min(n, MAX_ITER_N)):
        el = f.element(m)
        assert el - el == additive_identity


@pytest.mark.parametrize("n", SMALL_FIELDS)
def test_mul_identity(n):
    f = finite.Field(n)
    multiplicitive_identity = f.element(1)
    for m in range(n):
        el = f.element(m)
        x = el * multiplicitive_identity
        print(x)
        print(el.unreduced_mul(multiplicitive_identity))
        assert el * multiplicitive_identity == el


def test_aes_examples():
    """Examples from FIPS 197 (AES) section 4.2.1"""
    f = finite.Field(2 ** 8)
    assert f.mod_poly == [1, 1, 0, 1, 1, 0, 0, 0, 1]

    assert f.E(0x57) * f.E(0x01) == f.E(0x57)
    assert f.E(0x57) * f.E(0x02) == f.E(0xAE)
    assert f.E(0x57) * f.E(0x08) == f.E(0x8E)
    assert f.E(0x57) * f.E(0x10) == f.E(0x07)
    assert f.E(0x57) * f.E(0x13) == f.E(0xFE)

    assert f.E(0x57) * (f.E(0x01) + f.E(0x02) + f.E(0x10)) == f.E(0xFE)
    assert f.E(0x57) + f.E(0xAE) + f.E(0x07) == f.E(0xFE)


@pytest.mark.parametrize("n", SMALL_FIELDS)
def test_div_identity(n):
    f = finite.Field(n)
    multiplicitive_identity = f.element(1)
    for m in range(n):
        el = f.element(m)
        quot = el / multiplicitive_identity

        # repad quotient to same number of coefficients
        quot = quot + [0] * (f.power - len(quot))

        assert f.element(quot) == el


def evaluate_poly(poly, x):
    return sum(coeff * x ** k for k, coeff in enumerate(poly))


@pytest.mark.parametrize(
    "prime, power",
    itertools.chain(
        *(
            [(prime, power) for power in polys]
            for prime, polys in finite.POLY_MIN_WEIGHT.items()
        )
    ),
)
def test_polynomials_irreducible(prime, power):
    poly = finite.POLY_MIN_WEIGHT[prime][power]
    for n in range(-(prime - 1), prime):
        assert evaluate_poly(poly, n) != 0


def test_unreduced_multiplication():
    f = finite.Field(27)
    assert f.element([2, 1, 2]).unreduced_mul(f.element([2, 1, 2])) == [1, 1, 0, 1, 1]


def test_poly_divmod():
    num = [1, 5, 10, 10, 5, 1]
    den = [1, 2, 1]
    finite.poly_divmod(num, den)

    num = [5, 16, 10, 22, 7, 11, 1, 3]
    den = [1, 2, 1, 3]

    quot = [5, 1, 3, 0, 1]
    rem = [0, 5]

    q, r = finite.poly_divmod(num, den)
    assert quot == q
    assert rem == r
