import re

import pytest

import finite


@pytest.mark.parametrize(
    "n, ex_base, ex_pow",
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
def test_field_creation(n, ex_base, ex_pow):
    f = finite.Field(n)
    assert f.base == ex_base
    assert f.power == ex_pow


@pytest.mark.parametrize(
    "n, factorization",
    [
        (6, "2 * 3"),
        (10, "2 * 5"),
        (5040, "2**4 * 3**2 * 5 * 7"),
    ],
)
def test_bad_fields(n, factorization):
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
