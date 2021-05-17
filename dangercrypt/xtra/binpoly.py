class BinaryPolynomial:
    def __init__(self, value):
        if isinstance(value, int):
            self.value = value
            return
