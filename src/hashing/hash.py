# SHA-256 implementation

K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
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
        ^ (x >> 10)


def _sigma_1_256(x: int) -> int:
    block_size = 32
    return _rotate_right(x, 17, block_size)     \
        ^ _rotate_right(x, 19, block_size)      \
        ^ (x >> 3)


class HashingFactory:

    def hash(self, message: bytearray) -> bytearray:
        return bytearray()

    def _hash_message(self, message: bytearray) -> bytearray:
        pass
