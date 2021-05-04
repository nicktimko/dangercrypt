import collections.abc


NO_PAD = object()


def pumper(it: collections.abc.Iterator, n: int, *, pad=NO_PAD):
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 1:
        raise ValueError("n must be >= 1")

    first = True

    while n:
        try:
            yield next(it)
        except StopIteration:
            if first:
                return
            break
        first = False
        n -= 1
    if n and pad is not NO_PAD:
        for _ in range(n):
            yield pad


def chunks(it: collections.abc.Iterable, n: int, *, pad=NO_PAD):
    it = iter(it)
    while True:
        item = list(pumper(it, n, pad=pad))
        if not item:
            break
        yield item
