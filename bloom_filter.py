from ast import Lambda
import sys
from typing import List, Callable
from bitstring import BitArray
import mmh3
from fnvhash import fnv1_32


class BloomFilter:
    def __init__(self, size: int) -> None:
        self.bit_field = BitArray(uint=0, length=size)

    def read_bit(self, index: int) -> bool:
        return self.bit_field[index]

    def write_bit(self, index: int) -> bool:
        old_value = self.bit_field[index]
        self.bit_field[index] = self.bit_field[index] or 1
        return self.bit_field[index] != old_value

    def key_2_positions(
        self, hash_functions: List[Callable[[int, int], int]], seed: int, key: str
    ) -> List[int]:
        murmur_hash = mmh3.hash(key, seed)
        fnv_hash = fnv1_32(bytes(key, "utf-8"))
        return [h(murmur_hash, fnv_hash) for h in hash_functions]

    def init_hash_functions(
        self, num_hash_functions: int, num_bits: int
    ) -> List[Callable[[int, int], int]]:
        for i in range(num_hash_functions):
            yield lambda h1, h2: (h1 + i * h2 + i * i) % num_bits


if __name__ == "__main__":
    filter = BloomFilter(20)
    print(filter.write_bit(6))
    print(filter.write_bit(6))
    print(filter.read_bit(3))
