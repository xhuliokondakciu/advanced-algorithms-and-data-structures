import sys
from math import ceil, log
import random
from typing import List, Callable
from bitstring import BitArray
import mmh3
from fnvhash import fnv1_32


class BloomFilter:
    def _read_bit(self, index: int) -> bool:
        return self.bit_field[index]

    def _write_bit(self, index: int) -> bool:
        old_value = self.bit_field[index]
        self.bit_field[index] = self.bit_field[index] or 1
        return self.bit_field[index] != old_value

    def _key_2_positions(self, key: str) -> List[int]:
        murmur_hash = mmh3.hash(key, self.seed)
        fnv_hash = fnv1_32(bytes(key, "utf-8"))
        return [h(murmur_hash, fnv_hash) for h in self.hash_functions]

    def _init_hash_functions(
        self, num_hash_functions: int, num_bits: int
    ) -> List[Callable[[int, int], int]]:
        hash_generator = lambda i: lambda h1, h2: (h1 + i * h2 + i * i) % num_bits
        return [hash_generator(i) for i in range(num_hash_functions)]

    def contains(self, key: str) -> bool:
        return self._contains(self._key_2_positions(key))

    def _contains(self, positions: List[int]) -> bool:
        return all(self._read_bit(index) for index in positions)

    def insert(self, key: str):
        positions = self._key_2_positions(key)
        if not self._contains(positions):
            for index in positions:
                self._write_bit(index)

    def __init__(
        self,
        max_size: int,
        max_tolerance: int = 0.01,
        seed=random.randint(0, sys.maxsize),
    ) -> None:
        self.size = 0
        self.max_size = max_size
        self.seed = seed
        ln2 = log(2)

        # Optimal number of bits: m = - n * ln(p) / (ln(2))^2
        self.num_bits = -ceil(max_size * log(max_tolerance) / (ln2**2))
        if self.num_bits > sys.maxsize:
            raise ValueError(
                "Impossible to allocate enough memory for a Bloom filter satisfying requirements."
            )

        num_hash_func = -ceil(log(max_tolerance) / ln2)

        self.bit_field = BitArray(uint=0, length=self.num_bits)
        self.hash_functions: List[
            Callable[[int, int], int]
        ] = self._init_hash_functions(num_hash_func, self.num_bits)
