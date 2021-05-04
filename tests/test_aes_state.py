from dangercrypt.aes import State


def test_state_init():
    s = State()
    assert len(s.bytes) == s.n_bytes == s.rows * s.cols


def test_state_from_array():
    s = State.from_sq_array(range(16))
    for n in range(16):
        assert s.bytes[n] == n


def test_words():
    s = State.from_sq_array(range(16))
    assert s.words[0] == 0x00010203
    assert s.words[1] == 0x04050607
    assert s.words[2] == 0x08090A0B
    assert s.words[3] == 0x0C0D0E0F
