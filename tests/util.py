import collections.abc
import functools
import itertools
import operator
import random
import typing


MAX_ITER_N = 5000


def int_sampler(
    ranges: typing.Union[int, range, list[typing.Union[int, range]]],
    limit=MAX_ITER_N,
    seed=None,
) -> collections.abc.Generator[typing.Union[int, tuple[int, ...]]]:
    """
    Return integer permutations from the provided *ranges*. If there are more
    permutations than *limit*, sampling is used with no replacement.

    *seed* may be provided for repeatable tests. If sampling isn't used, this
    argument has no effect.

    If ranges is a scalar integer or lone range object, the items yielded will be
    individual integers, otherwise they are tuples.
    """
    scalar_range = isinstance(ranges, (int, range))
    if scalar_range:
        ranges = [ranges]

    # total number of permutations bigger than the limit?
    ranges = [range(r) if not isinstance(r, range) else r for r in ranges]
    range_lens = [len(r) for r in ranges]
    permutations = functools.reduce(operator.mul, range_lens)
    if permutations <= limit:
        # do 'em all (delegate to a returned generator)
        if scalar_range:
            yield from ranges[0]
        else:
            yield from itertools.product(*ranges)
        return

    # only do some
    rng = random.Random()
    rng.seed(seed or sum(str(ranges).encode()))
    samples = rng.sample(range(permutations), limit)

    # decompose samples into the indexes of respective ranges
    for s in samples:
        decomposed = []
        for r in ranges:
            s, x = divmod(s, len(r))
            decomposed.append(r[x])
        if scalar_range:
            yield decomposed[0]
        else:
            yield tuple(decomposed)
