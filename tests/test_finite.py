import itertools
import operator
import random
import re

import pytest

import finite


SMALL_FIELDS = [2, 3, 4, 5, 7, 8, 9, 11, 13, 16, 17, 19, 23, 25, 27]


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


@pytest.mark.parametrize("n", SMALL_FIELDS)
def test_element_roundtrip(n):
    f = finite.Field(n)
    for m in range(n):
        el = f.element(m)
        assert int(el) == m


@pytest.mark.parametrize("n", SMALL_FIELDS)
def test_characteristic(n):
    f = finite.Field(n)
    for m in range(n):
        el = f.element(m)
        assert sum(el for _ in range(f.prime)) == f.element(0)


@pytest.mark.parametrize("n", SMALL_FIELDS)
@pytest.mark.parametrize("func", [operator.add, operator.sub])
def test_add_identity(n, func):
    f = finite.Field(n)
    additive_identity = f.element(0)
    for m in range(n):
        el = f.element(m)
        assert func(el, additive_identity) == el



@pytest.mark.parametrize("n", SMALL_FIELDS)
def test_add_inverse(n):
    f = finite.Field(n)
    additive_identity = f.element(0)
    for m in range(n):
        el = f.element(m)
        assert el + (-el) == additive_identity


@pytest.mark.parametrize("func", [operator.add, operator.mul])
@pytest.mark.parametrize("n", SMALL_FIELDS)
def test_commutative(n, func):
    f = finite.Field(n)
    for na, nb in itertools.product(range(n), range(n)):
        a = f.element(na)
        b = f.element(nb)
        assert func(a, b) == func(b, a), (a, b)


@pytest.mark.parametrize("func", [operator.add, operator.mul])
@pytest.mark.parametrize("n", SMALL_FIELDS)
def test_associative(n, func):
    f = finite.Field(n)
    if n**3 > 1000:
        rng = random.Random()
        rng.seed(n)
        def _gen():
            yield rng.randrange(n), rng.randrange(n), rng.randrange(n)
        gen = _gen()
    else:
        gen = itertools.product(range(n), range(n), range(n))

    for na, nb, nc in gen:
        print(na, nb, nc)
        a = f.element(na)
        b = f.element(nb)
        c = f.element(nc)
        assert func(func(a, b), c) == func(a, func(b, c)), (a, b, c)


@pytest.mark.parametrize("n", SMALL_FIELDS)
def test_sub(n):
    f = finite.Field(n)
    additive_identity = f.element(0)
    for m in range(n):
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


@pytest.mark.xfail(reason="dunno...")
def test_aes_mul():
    f = finite.Field(2**8)
    assert f.mod_poly == [1, 1, 0, 1, 1, 0, 0, 0, 1]

    assert f.element(0x57) * f.element(0x01) == f.element(0x57)
    assert f.element(0x57) * f.element(0x02) == f.element(0xAE)
    assert f.element(0x57) * f.element(0x10) == f.element(0x07)
    assert f.element(0x57) * f.element(0x13) == f.element(0xFE)


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
