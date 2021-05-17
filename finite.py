import collections
import math


T_POLY = list[int]


def get_prime_factors(number):
    # https://paulrohan.medium.com/111de56541f

    prime_factors = []

    while number % 2 == 0:
        prime_factors.append(2)
        number = number / 2

    for i in range(3, int(math.sqrt(number)) + 1, 2):
        while number % i == 0:
            prime_factors.append(int(i))
            number = number / i

    if number > 2:
        prime_factors.append(int(number))

    return prime_factors


UNICODE_SUPERSCRIPTS = {
    ord("0"): "\N{SUPERSCRIPT ZERO}",
    ord("1"): "\N{SUPERSCRIPT ONE}",
    ord("2"): "\N{SUPERSCRIPT TWO}",
    ord("3"): "\N{SUPERSCRIPT THREE}",
    ord("4"): "\N{SUPERSCRIPT FOUR}",
    ord("5"): "\N{SUPERSCRIPT FIVE}",
    ord("6"): "\N{SUPERSCRIPT SIX}",
    ord("7"): "\N{SUPERSCRIPT SEVEN}",
    ord("8"): "\N{SUPERSCRIPT EIGHT}",
    ord("9"): "\N{SUPERSCRIPT NINE}",
    ord("+"): "\N{SUPERSCRIPT PLUS SIGN}",
    ord("-"): "\N{SUPERSCRIPT MINUS}",
}


def int2sup(n: int) -> str:
    """
    Integer to superscripts
    """
    return str(n).translate(UNICODE_SUPERSCRIPTS)


POLY_MIN_WEIGHT = {
    # Hansen and Mullen. Supplement to Primitive Polynomials over Finite Fields
    # https://www.ams.org/journals/mcom/1992-59-200/S0025-5718-1992-1134730-7/S0025-5718-1992-1134730-7.pdf
    2: {
        2: [1, 1, 1],
        3: [1, 1, 0, 1],
        4: [1, 1, 0, 0, 1],
        5: [1, 0, 1, 0, 0, 1],
        6: [1, 0, 1, 0, 0, 0, 1],
        7: [1, 1, 0, 0, 0, 0, 0, 1],
        # 8: [1, 0, 1, 1, 1, 0, 0, 0, 1],  # from paper
        8: [1, 1, 0, 1, 1, 0, 0, 0, 1],  # AES
    },
    3: {
        2: [2, 1, 1],
        3: [1, 2, 0, 1],
        4: [2, 1, 0, 0, 1],
        5: [1, 2, 0, 0, 0, 1],
    },
    5: {
        2: [2, 1, 1],
        3: [2, 3, 0, 1],
        4: [2, 2, 1, 0, 1],
        5: [2, 4, 0, 0, 0, 1],
    },
    7: {
        2: [3, 1, 1],
        3: [2, 3, 0, 1],
        4: [5, 3, 1, 0, 1],
        5: [4, 1, 0, 0, 0, 1],
    },
    11: {
        2: [7, 1, 1],
        3: [4, 1, 0, 1],
    },
    13: {
        2: [2, 1, 1],
        3: [6, 1, 0, 1],
    },
    17: {
        2: [3, 1, 1],
        3: [3, 1, 0, 1],
    },
    19: {
        2: [2, 1, 1],
        3: [4, 1, 0, 1],
    },
    23: {
        2: [7, 1, 1],
        3: [3, 1, 0, 1],
    },
}


class Field:
    def __init__(self, n, mod_poly=None):
        self.n = n

        factors = collections.Counter(get_prime_factors(n))
        if len(factors) > 1:
            factorization = " * ".join(
                f"{b}{int2sup(p)}" if p > 1 else f"{b}"
                for b, p in sorted(factors.items())
            )
            raise ValueError(f"cannot form GF({n}) = GF({factorization})")

        (self.prime, self.power), *_ = factors.items()
        if self.power == 1:
            self.mod_poly = [1]
        else:
            if mod_poly is None:
                try:
                    self.mod_poly = POLY_MIN_WEIGHT[self.prime][self.power]
                except KeyError:
                    self.mod_poly = None
                    # raise Exception(
                    #     f"don't know a primitive polynomial for GF({self.prime}{int2sup(self.power)})"
                    # )
            else:
                self.mod_poly = mod_poly

    def __repr__(self):
        if self.power == 1:
            return f"{self.__class__.__name__}({self.prime})"
        return f"{self.__class__.__name__}({self.prime}{int2sup(self.power)})"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError
        return (self.prime, self.power) == (other.prime, other.power)

    def element(self, value):
        return Element(self, value)

    E = element


class Element:
    def __init__(self, field, value):
        self.field = field
        if isinstance(value, int):
            coeff = []
            quotient = value
            for _ in range(field.power):
                quotient, coeff_n = divmod(quotient, field.prime)
                coeff.append(coeff_n)
            if quotient:
                raise ValueError(f"{self.field} can not hold {value}")
        else:
            coeff = value
            coeff = [c % self.field.prime for c in coeff]
            if len(coeff) != field.power:
                raise ValueError(
                    f"number of coefficients: {len(coeff)} disagrees with field exponent: {field.power}"
                )

        self.coeff = coeff

    def __repr__(self):
        return f"<{self.__class__.__name__} in {self.field} coeff={self.coeff}>"

    def __add__(self, other):
        new_coeff = [
            (a + b) % self.field.prime for a, b in zip(self.coeff, other.coeff)
        ]
        return self.__class__(self.field, new_coeff)

    def __radd__(self, other):
        if other == 0:
            # this enables using sum() on an iterable of Elements
            return self
        raise TypeError("unsupported")  # could probably support...

    def __sub__(self, other):
        new_coeff = [
            (a - b) % self.field.prime for a, b in zip(self.coeff, other.coeff)
        ]
        return self.__class__(self.field, new_coeff)

    def __neg__(self):
        return self.__class__(self.field, 0) - self

    def __int__(self):
        return sum(c * self.field.prime ** p for p, c in enumerate(self.coeff))

    def __eq__(self, other):
        return self.field == other.field and self.coeff == other.coeff

    def __divmod__(self, other):
        quotient, remainder = poly_divmod(self.coeff, other.coeff)

        # re-pad remainder to same number of coefficients
        remainder = pad(remainder, self.field.power)

        # the quotient isn't sure to fit in the field, but the remainder will, so
        # return the former as a generic polynomial, and the remainder as an Element.
        return quotient, self.__class__(self.field, remainder)

    def __truediv__(self, other):
        return divmod(self, other)[0]

    def __mod__(self, other):
        return divmod(self, other)[1]

    def unreduced_mul(self, other):
        result = [0] * (2 * self.field.power - 1)
        for exp_a, coef_a in enumerate(self.coeff):
            for exp_b, coef_b in enumerate(other.coeff):
                result[exp_a + exp_b] += coef_a * coef_b
        result = [n % self.field.prime for n in result]
        return result

    def __mul__(self, other):
        raw = self.unreduced_mul(other)
        if self.field.power > 1:
            _quotient, remainder = poly_divmod(raw, self.field.mod_poly)
            remainder = pad(remainder, self.field.power)
        else:
            remainder = [raw[0] % self.field.prime]
        return self.__class__(self.field, remainder)


def normalize(poly: T_POLY) -> None:
    """Normalize (remove max order 0's) *poly* in-place."""
    while poly and poly[-1] == 0:
        poly.pop()
    if poly == []:
        poly.append(0)


def pad(poly: T_POLY, order: int) -> T_POLY:
    """Pad the *poly* out to *order*, return a new copy."""
    return poly + [0] * (order - len(poly))


def poly_divmod(num: T_POLY, den: T_POLY) -> tuple[T_POLY, T_POLY]:
    """
    Polynomial long division

    From http://stackoverflow.com/questions/26173058/division-of-polynomials-in-python

    A polynomial is represented by a list of its coefficients, eg
    5*x**3 + 4*x**2 + 1 -> [1, 0, 4, 5]

    Modified by PM 2Ring 2014.10.03
    Modified by NickT to work with integers only
    """
    # Create normalized copies of the args
    num = num[:]
    normalize(num)
    den = den[:]
    normalize(den)

    if len(num) >= len(den):
        # Shift den towards right so it's the same degree as num
        shiftlen = len(num) - len(den)
        den = [0] * shiftlen + den
    else:
        return [0], num

    quotient = []
    divisor = den[-1]  # removed float
    for i in range(shiftlen + 1):
        # Get the next coefficient of the quotient.
        mult = num[-1] // divisor  # truncating division
        quotient = [mult] + quotient

        # Subtract mult * den from num, but don't bother if mult == 0
        # Note that when i==0, mult!=0; so quot is automatically normalized.
        if mult != 0:
            d = [mult * u for u in den]
            num = [u - v for u, v in zip(num, d)]

        num.pop()
        den.pop(0)

    normalize(num)
    return quotient, num
