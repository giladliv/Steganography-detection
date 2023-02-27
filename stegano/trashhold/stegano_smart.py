from textwrap import wrap

from numpy import random
from typing import List, Tuple
import numpy as np
# import cv2.load_config_py2
import cv2

BITS_IN_BYTE = 8
PIX_BYTE_LEN = BITS_IN_BYTE
LEN_PIX = 3
MOD = 2 ** 4


def int_to_bin(num: int, n: int = 0):
    return format(num, 'b').zfill(n)


def split_str_by_chunks(s: str, n: int):
    return [s[i: i + n] for i in range(0, len(s), n)]


def get_file_bin_by_chunks(file_name):
    pass


# print(int_to_bin(37))
# print(split_str_by_chunks("123456789" * 2, 2))
# s = "123456789" * 2
# print(s[:-1])


def change_num_ending(og_num: int, bin_str: str):
    num_str = int_to_bin(og_num, PIX_BYTE_LEN)
    num_str = num_str[: - len(bin_str)] + bin_str
    return num_str


def show_change(og_num: int, bin_str: str):
    print(int_to_bin(og_num, PIX_BYTE_LEN))
    print(change_num_ending(og_num, bin_str))


def pix_list_to_list(pix_list: List[Tuple[int]]) -> List[int]:
    list_total = []
    for pix in pix_list:
        list_total += list(pix)
    return list_total


def list_to_tup_list(lst: List[int], n: int = 1) -> List[Tuple[int]]:
    list_tup = [tuple(lst[i: i + n]) for i in range(0, len(lst), n)]
    if len(list_tup) > 0 and len(list_tup[-1]) < n:
        diff = n - len(list_tup[-1])
        list_tup[-1] += tuple([0] * diff)
    return list_tup


def list_to_pix_list(lst: List[int]) -> List[Tuple[int]]:
    return list_to_tup_list(lst, LEN_PIX)


# pix_list = [(27, 64, 164), (248, 244, 194), (174, 246, 250), (149, 95, 232),
#             (188, 156, 169), (71, 167, 127), (132, 173, 97), (113, 69, 206),
#             (255, 29, 213), (53, 153, 220), (246, 225, 229), (142, 82, 175)]
#
# print(pix_list_to_list(pix_list))
# reg_list = pix_list_to_list(pix_list)
# print(list_to_pix_list([]))


def bytes_from_file(filename):
    try:
        with open(filename, "rb") as f:
            # do while loop
            list_bytes = f.read()
    except:
        list_bytes = []

    return list_bytes


def byte_to_str_bin(byte):
    return int_to_bin(int(byte), BITS_IN_BYTE)


def file_to_bin_str(filename):
    list_bytes_int = bytes_from_file(filename)
    list_btye_str = [byte_to_str_bin(byte) for byte in list_bytes_int]
    return ''.join(list_btye_str)


# list_bytes = bytes_from_file("try.exe")
# print(list_bytes, f'\n{len(list_bytes)} {len(list_bytes) * 8}')
#
# list_bytes = file_to_bin_str("try.exe")
# print(list_bytes, f'\n{len(list_bytes)}')


# list_bytes = bytes_from_file("data/try.txt")
# print(list_bytes, f'\n{len(list_bytes)} {len(list_bytes) * 8}')


# take a string of the injection and taking the real value and return its value
def insert_data(num: int, inj: str, mod: int = MOD):
    inj = int(inj, 2) % mod
    return int(num / mod) * mod + inj


# inject the data to the picture
def inject_data_to_pixels(pic: np.ndarray, inj_list: list, mod: int = MOD) -> np.ndarray:
    pic = pic.copy()
    pic_lined = pic.ravel()
    max_size = len(inj_list)
    for i in range(min(max_size, pic.size)):
        pic_lined[i] = insert_data(pic_lined[i], inj_list[i], mod=mod)
    return pic


# # inject the data to the picture
# def inject_data_to_pixels(pic: np.ndarray, inj_list: list, mod: int = MOD) -> np.ndarray:
#     pic = pic.copy()
#     counter = 0     # index for the injection
#     max_size = len(inj_list)
#     row, col, inner = pic.shape
#     for i in range(row):
#         for j in range(col):
#             for k in range(inner):
#                 if counter == max_size:
#                     return pic
#                 pic[i][j][k] = insert_data(pic[i][j][k], inj_list[counter], mod=mod)
#                 counter += 1
#     return pic

# futrue function:

# # get a binary data from file
# list_bytes = file_to_bin_str("data/try.txt")
# list_bytes += int_to_bin(0, BITS_IN_BYTE)
# print(list_bytes, f'\n{len(list_bytes)}\n')
# # divide it to groups by number of bytes
# parted_data = split_str_by_chunks(list_bytes, 4)
# print(parted_data)
#
# rows = 4
# cols = 3
# MAX_NUMS = 256
# PXL_FORM = 3
#
# im_arr = random.randint(MAX_NUMS, size=(rows, cols, PXL_FORM))
# print(im_arr.shape)
# print(type(im_arr))
# print('real:\n', im_arr)
# steg_enc = inject_data_to_pixels(im_arr, parted_data)
# print('enc:\n', steg_enc)
#
# # ravel is iterable array that is 1-d  while the original form is not changed
# print(steg_enc.ravel())
# total = ''
# for num in steg_enc.ravel():
#     total += int_to_bin(num % MOD, 4)
#
# hidden = ''
# for n in wrap(total, 8):
#     n = int(n, 2)
#     if n == 0:
#         break
#     hidden += chr(n)
#
# print('hidden:\t', hidden)
# temp = im_arr.ravel()
# temp[0] = 666
#
# print(im_arr.size)


class SteganoImage:
    def __init__(self, pic_file, data_file, lsb: int = 4):
        self.lsb = lsb
        self.mod = 2 ** self.lsb
        self.pic_file = pic_file
        self.data_file = data_file
        self.im_arr = cv2.imread(pic_file)
        # print(self.im_arr)
        self.list_bytes = file_to_bin_str(data_file)
        self.list_bytes += int_to_bin(0, BITS_IN_BYTE)
        # print(self.list_bytes, f'\n{len(self.list_bytes)}\n')
        # divide it to groups by number of bytes

    def perform_stegano(self, name: str):
        parted_data = split_str_by_chunks(self.list_bytes, self.lsb)
        #print(parted_data)
        steg = inject_data_to_pixels(self.im_arr, parted_data, mod=self.mod)
        # ravel is iterable array that is 1-d  while the original form is not changed
        cv2.imwrite(name, steg)


    def get_data(self, name):
        img = cv2.imread(name)
        total = ''
        hidden = ''
        for num in img.ravel():
            total += int_to_bin(num % self.mod, self.lsb)
            if len(total) == BITS_IN_BYTE:
                #print(total)
                n = int(total, 2)
                total = ''
                if n == 0:
                    break

                hidden += chr(n)

        # print('hidden:\t', hidden)
        return hidden

steg_enc = SteganoImage("../data/abc.jpg", "data/alice_in_wonderland.txt")
steg_enc.perform_stegano("data/a.png")
steg_enc.get_data("data/a.png")
print(steg_enc.im_arr.size)

