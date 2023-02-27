import glob
import sys
from functools import reduce
import random
from typing import List, Tuple
import numpy as np


class utils:
    BITS_IN_BYTE = 8
    PIX_BYTE_LEN = BITS_IN_BYTE
    LEN_PIX = 3
    MOD = 2 ** 4
    PRNT_ABL_CH = [i.to_bytes(1, 'big') for i in range(128) if chr(i).isprintable()]
    BIN = [i.to_bytes(1, 'big') for i in range(255)]

    @staticmethod
    def int_to_bin(num: int, n: int = 0):
        return format(num, 'b').zfill(n)

    @staticmethod
    def split_str_by_chunks(s: str, n: int):
        return [s[i: i + n] for i in range(0, len(s), n)]

    @staticmethod
    def change_num_ending(og_num: int, bin_str: str):
        num_str = utils.int_to_bin(og_num, utils.PIX_BYTE_LEN)
        num_str = num_str[: - len(bin_str)] + bin_str
        return num_str

    @staticmethod
    def show_change(og_num: int, bin_str: str):
        print(utils.int_to_bin(og_num, utils.PIX_BYTE_LEN))
        print(utils.change_num_ending(og_num, bin_str))

    @staticmethod
    def pix_list_to_list(pix_list: List[Tuple[int]]) -> List[int]:
        list_total = []
        for pix in pix_list:
            list_total += list(pix)
        return list_total

    @staticmethod
    def list_to_tup_list(lst: List[int], n: int = 1) -> List[Tuple[int]]:
        list_tup = [tuple(lst[i: i + n]) for i in range(0, len(lst), n)]
        if len(list_tup) > 0 and len(list_tup[-1]) < n:
            diff = n - len(list_tup[-1])
            list_tup[-1] += tuple([0] * diff)
        return list_tup

    @staticmethod
    def list_to_pix_list(lst: List[int]) -> List[Tuple[int]]:
        return utils.list_to_tup_list(lst, utils.LEN_PIX)

    @staticmethod
    def bytes_from_file(filename):
        try:
            with open(filename, "rb") as f:
                # do while loop
                list_bytes = f.read()
        except:
            list_bytes = []

        return list_bytes

    @staticmethod
    def byte_to_str_bin(byte):
        return utils.int_to_bin(int(byte), utils.BITS_IN_BYTE)

    @staticmethod
    def file_to_bin_str(filename):
        list_bytes_int = utils.bytes_from_file(filename)
        list_btye_str = [utils.byte_to_str_bin(byte) for byte in list_bytes_int]
        return ''.join(list_btye_str)

    # take a string of the injection and taking the real value and return its value
    @staticmethod
    def insert_data(num: int, inj: str, mod: int = MOD):
        inj = int(inj, 2) % mod
        return int(num / mod) * mod + inj

    # inject the data to the picture
    @staticmethod
    def inject_data_to_pixels(pic: np.ndarray, inj_list: list, mod: int = MOD) -> np.ndarray:
        pic = pic.copy()
        pic_lined = pic.ravel()
        max_size = min(len(inj_list), pic.size)
        for i in range(max_size):
            if inj_list[i] is None:
                continue
            pic_lined[i] = utils.insert_data(pic_lined[i], inj_list[i], mod=mod)
        return pic

    @staticmethod
    def prod_tuple(val):
        return reduce((lambda x, y: x * y), val)

    @staticmethod
    def crt_random_prnt_bin(n):
        return b''.join(random.choices(utils.PRNT_ABL_CH, k=n))

    @staticmethod
    def bin_random_prnt(n: int = None):
        if n is None or n <= 0:
            n = sys.maxsize
        return utils.crt_random_prnt_bin(random.randint(1, n))

    @staticmethod
    def crt_random_all_bin(n):
        return b''.join(random.choices(utils.BIN, k=n))

    @staticmethod
    def bin_random_all(n: int = None):
        if n is None or n <= 0:
            n = sys.maxsize
        return utils.crt_random_all_bin(random.randint(1, n))


