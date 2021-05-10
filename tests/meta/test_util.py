import pytest

from tests.util import int_sampler


def test_sampler_basic():
    it = int_sampler([2, 2], limit=100)
    assert next(it) == (0, 0)
    assert next(it) == (0, 1)
    assert next(it) == (1, 0)
    assert next(it) == (1, 1)
    with pytest.raises(StopIteration):
        next(it)


@pytest.mark.parametrize("dim", [1, 2, 3, 5, 10])
@pytest.mark.parametrize("limitpad", [0, 1])
@pytest.mark.parametrize("type_", [int, range])
def test_sampler_varying_dims(dim, limitpad, type_):
    size = 2 ** dim

    ranges = [2] * dim
    ranges = [type_(r) for r in ranges]

    gen = int_sampler(ranges, limit=size + limitpad)
    combos = list(gen)

    assert len(combos) == size
    assert len(set(combos)) == size
    assert min(combos) == (0,) * dim
    assert max(combos) == (1,) * dim


@pytest.mark.parametrize("dim", [1, 2, 3, 5, 10])
def test_sampler_sampling(dim):
    size = 2 ** dim
    gen = int_sampler([2] * dim, limit=size - 1)
    combos = list(gen)

    assert len(combos) == size - 1
    assert len(set(combos)) == size - 1
    assert min(combos) in {(0,) * dim, (0,) * (dim - 1) + (1,)}
    assert max(combos) in {(1,) * dim, (1,) * (dim - 1) + (0,)}


@pytest.mark.parametrize(
    "dims, size",
    [
        ([1], 1),
        ([2], 2),
        ([10], 10),
        ([1, 2, 3], 6),
        ([1, 2, 3, 4], 24),
        ([1, 2, 3, 4, 5], 120),
    ],
)
def test_sampler_heterodim(dims, size):
    it = int_sampler(dims, limit=size)

    assert sum(1 for _ in it) == size


@pytest.mark.parametrize("mode", ["sampling", "complete"])
@pytest.mark.parametrize("type_", [int, range, "sparse_range"])
def test_sampler_scalar2scalar(mode, type_):
    """When provided a scalar as the 'ranges', yield scalars."""
    size = 4
    if type_ == "sparse_range":
        notranges = range(0, size * 2, 2)
    else:
        notranges = type_(size)

    limit_tweak = -1 if mode == "sampling" else 0

    it = int_sampler(notranges, limit=size + limit_tweak)

    for x in it:
        assert type(x) is int
