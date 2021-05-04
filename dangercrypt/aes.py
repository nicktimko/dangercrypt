import math

from dangercrypt import xtra


AES_ROWS = 4
AES_COLS = 4
AES_BYTE_SIZE = 8


class State:
    """
    FIPS 197 AES, sec. 3.4

        s[r, c]= in[r + 4c]   (aka iterate down the columns first)

    """

    def __init__(self, *, rows=AES_ROWS, cols=AES_COLS, byte_size=AES_BYTE_SIZE):
        self.rows = rows
        self.cols = cols
        self.n_bytes = rows * cols

        self.bytes = list([0] * self.n_bytes)

        self.byte_size = byte_size

    @classmethod
    def from_sq_array(cls, input_):
        rows = cols = int(math.sqrt(len(input_)))

        if rows * cols != len(input_):
            raise ValueError("input array must be square")

        state = cls(rows=rows, cols=cols)

        assert len(state.bytes) == len(input_)

        state.bytes = list(input_)
        return state

    @property
    def words(self):
        return list(
            xtra.math.bytes_to_word(bb, self.byte_size)
            for bb in xtra.itertools.chunks(self.bytes, self.rows)
        )
