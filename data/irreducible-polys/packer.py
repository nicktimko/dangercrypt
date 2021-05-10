import argparse
import json
import pathlib
import sys


PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 27]
THIS_DIR = pathlib.Path(__file__).parent


def find_path(n):
    matches = list(THIS_DIR.glob(f"F{n}-*.txt"))
    if len(matches) == 1:
        return matches[0]
    elif matches:
        raise Exception(f"multiple matches for n={n}")
    else:
        raise Exception(f"can't find any files for n={n}")


def process_line(line, format_):
    if format_ == 2:
        return process_line_2(line)
    if format_ in PRIMES:
        return process_line_prime(line)
    return process_line_primepower(line)


def process_line_2(line):
    powers = [int(x) for x in line.split(",")]
    order, *others = powers
    dcoeffs = {o: 1 for o in others}
    dcoeffs[order] = 1
    return order, dcoeffs


def process_line_prime(line):
    dcoeffs = {}
    order, other_coeffs = line.split(",", maxsplit=1)
    order = int(order)

    dcoeffs[order] = 1

    for other_coeff in other_coeffs.strip().split(","):
        assert other_coeff[-1] == ")"
        power, coeff = (int("0" + x) for x in other_coeff.rstrip(")").split("("))
        dcoeffs[power] = coeff

    return order, dcoeffs


def coeff_dict2list(dcoeffs, order=None):
    """convert dictionary of coefficients to list"""
    if order is None:
        order = max(dcoeffs)
    coeffs = []
    for n in range(order):
        coeffs.append(dcoeffs.get(n+1, 0))
    return coeffs


def process_file(n):
    path = find_path(n)
    for x, line in enumerate(open(path, mode="r")):
        yield process_line(line, n)
        # yield coeff_dict2list(poly, order=order)


def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument("n", type=int)
    args = parser.parse_args()

    data = {}
    for p in PRIMES[:-1]:
        data[p] = dict(process_file(p))

    with open("data.json", mode="w") as f:
        json.dump(data, f)


if __name__ == "__main__":
    sys.exit(main())
