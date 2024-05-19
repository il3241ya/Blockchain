# SHA-256 implementation

constants = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
    0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]


# cyclic bit rotation to the right
def _rotate_right(block: int, shift: int, block_size: int) -> int:
    shift = shift % block_size
    return (block >> shift) | (block << (block_size - shift))


# cyclic bit rotation to the left
def _rotate_left(block: int, shift: int, block_size: int) -> int:
    shift = shift % block_size
    return (block << shift) | (block >> (block_size - shift))


def _ch(x: int, y: int, z: int) -> int:
    return (x & y) ^ (~x & z)


def _maj(x: int, y: int, z: int) -> int:
    return (x & y) ^ (x & z) ^ (y & z)


def _sum_0_256(x: int) -> int:
    block_size = 32
    return _rotate_right(x, 2, block_size)      \
        ^ _rotate_right(x, 13, block_size)      \
        ^ _rotate_right(x, 22, block_size)


def _sum_1_256(x: int) -> int:
    block_size = 32
    return _rotate_right(x, 6, block_size)      \
        ^ _rotate_right(x, 11, block_size)      \
        ^ _rotate_right(x, 25, block_size)


def _sigma_0_256(x: int) -> int:
    block_size = 32
    return _rotate_right(x, 7, block_size)      \
        ^ _rotate_right(x, 18, block_size)      \
        ^ (x >> 3)


def _sigma_1_256(x: int) -> int:
    block_size = 32
    return _rotate_right(x, 17, block_size)     \
        ^ _rotate_right(x, 19, block_size)      \
        ^ (x >> 10)


class HashingFactory:

    def hash(self, message: bytearray | str | bytes) -> bytearray:
        message = self._pad(self._convert(message))
        # initial hash state
        hash_words = [
            0x6a09e667,     # h0
            0xbb67ae85,     # h1
            0x3c6ef372,     # h2
            0xa54ff53a,     # h3
            0x510e527f,     # h4
            0x9b05688c,     # h5
            0x1f83d9ab,
            0x5be0cd19
        ]

        for block in [message[i:i + 64] for i in range(0, len(message), 64)]:
            message_schedule = self._schedule(block)

            a, b, c, d, e, f, g, h = hash_words

            for t in range(64):
                t1 = self._get_t1(h, e, f, g, t, message_schedule)
                t2 = self._get_t2(a, b, c)

                h, g, f, e, d, c, b, a = g, f, e, (d + t1) % (1 << 32), \
                    c, b, a, (t1 + t2) % (1 << 32)

            i = 0
            for var in [a, b, c, d, e, f, g, h]:
                hash_words[i] = (hash_words[i] + var) % (1 << 32)
                i += 1

        out = bytearray()
        for word in hash_words:
            out += bytearray(word.to_bytes(4))
        return out

    def _convert(self, message: bytearray | str | bytes) -> bytearray:
        # convert input to bytearray
        if isinstance(message, str):
            message = bytearray(message, 'ascii')
        if isinstance(message, bytes):
            message = bytearray(message)
        if isinstance(message, bytearray):
            return message
        raise ValueError(f'message has unsupported type: {type(message)}')

    def _pad(self, message: bytearray) -> bytearray:
        # pad message so it can be split in 32 byte chunks
        length = len(message) * 8   # in bits
        message.append(0x80)
        while (len(message) + 8) % 64:
            message.append(0x00)
        # append length of initial message as 8 byte integer
        message += length.to_bytes(length=8)
        return message

    def _schedule(self, block: bytearray) -> list[int]:
        message_schedule = []
        for t in range(64):
            if t <= 15:
                message_schedule.append(bytes(
                    block[t * 4:(t * 4) + 4]))
            else:
                terms = []
                terms.append(_sigma_1_256(
                    int.from_bytes(message_schedule[t - 2])))
                terms.append(int.from_bytes(message_schedule[t - 7]))
                terms.append(_sigma_0_256(
                    int.from_bytes(message_schedule[t - 15])))
                terms.append(int.from_bytes(message_schedule[t - 16]))

                schedule = (sum(terms) % (1 << 32)).to_bytes(4)
                message_schedule.append(schedule)
        return message_schedule

    def _get_t1(
        self,
        h: int,
        e: int,
        f: int,
        g: int,
        round: int,
        message_schedule: list[int]
    ) -> int:
        return (h + _sum_1_256(e) + _ch(e, f, g) + constants[round]
                + int.from_bytes(message_schedule[round])) % (1 << 32)

    def _get_t2(self, a: int, b: int, c: int) -> int:
        return (_sum_0_256(a) + _maj(a, b, c)) % (1 << 32)
