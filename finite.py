import collections
import math


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


class Field:
    def __init__(self, n):
        self.n = n
        factors = collections.Counter(get_prime_factors(n))
        if len(factors) > 1:
            factorization = " * ".join(
                f"{b}**{p}" if p > 1 else f"{b}" for b, p in factors.items()
            )
            raise ValueError(f"cannot form GF({n}) = GF({factorization})")

        (self.base, self.power), *_ = factors.items()

    def __repr__(self):
        if self.power == 1:
            return f"{self.__class__.__name__}({self.base})"
        return f"{self.__class__.__name__}({self.base}**{self.power})"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError
        return (self.base, self.power) == (other.base, other.power)

    def element(self, value):
        return Element(self, value)


class Element:
    def __init__(self, field, value):
        self.field = field
        if isinstance(value, int):
            coeff = []
            quotient = value
            for _ in range(field.power):
                quotient, coeff_n = divmod(quotient, field.base)
                coeff.append(coeff_n)
            if quotient:
                raise ValueError(f"{self.field} can not hold {value}")
        else:
            coeff = value
            if len(coeff) != field.power:
                raise ValueError(
                    f"number of coefficients: {len(coeff)} disagrees with field exponent: {field.power}"
                )

        self.coeff = coeff

    def __repr__(self):
        return f"<{self.__class__.__name__} coeff={self.coeff}>"

    def __add__(self, other):
        new_coeff = [(a + b) % self.field.base for a, b in zip(self.coeff, other.coeff)]
        return self.__class__(self.field, new_coeff)

    def __mul__(self, other):
        result = [0] * (2 * self.field.power - 1)
        for exp_a, coef_a in enumerate(self.coeff):
            for exp_b, coef_b in enumerate(other.coeff):
                result[exp_a + exp_b] += coef_a + coef_b
            print(result)
        result = [n % self.field.base for n in result]
        return result
