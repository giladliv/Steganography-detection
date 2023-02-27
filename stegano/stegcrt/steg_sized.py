from math import log2, ceil

import numpy

from utils import *
from stegcrt.steg_lsb import SteganoImageBaseLSB


class SteganoImageBaseSizedLSB(SteganoImageBaseLSB):
    NUM_BYTES = 4

    def __init__(self, pic_file, data_file, lsb: int = 4, use_shape_size: bool = False):
        super().__init__(pic_file, data_file, lsb=lsb)
        self.get_max_size_space(use_shape_size)


    def get_max_size_space(self, use_shape_size: bool):
        self.start_bytes = self.NUM_BYTES
        self.free_space = utils.prod_tuple(self.im_arr.shape)
        if use_shape_size:
            # get the number of bits in from the size and divide by 8 to get number of bytes
            self.start_bytes = ceil(log2(self.free_space) / utils.BITS_IN_BYTE)
        self.free_space -= self.start_bytes
        self.num_bits_size = self.start_bytes * utils.BITS_IN_BYTE


    def parted_data_alg(self):
        parted_data = utils.split_str_by_chunks(self.list_bytes, self.lsb)
        len_bits, arr_bits = self.arr_parted_size()
        parted_data = arr_bits + parted_data[:len_bits]
        return parted_data, len_bits

    def recover_data(self, img):
        total = ''
        hidden = bytes()
        pix_for_size = int(self.num_bits_size / self.lsb)
        pix_lined = img.ravel()
        for pixel in pix_lined[:pix_for_size]:
            total += utils.int_to_bin(pixel % self.mod, self.lsb)
        num_of_pix = int(total, 2)

        total = ''
        for pixel in pix_lined[pix_for_size: pix_for_size + num_of_pix]:
            total += utils.int_to_bin(pixel % self.mod, self.lsb)
            if len(total) == utils.BITS_IN_BYTE:
                hidden += int(total, 2).to_bytes(1, 'big')
                total = ''
        return hidden

    def arr_parted_size(self):
        len_bits = min(len(self.list_bytes), self.free_space)
        len_bits = int(len_bits / self.lsb)
        bin_len = utils.int_to_bin(len_bits, self.num_bits_size)
        arr_bits = utils.split_str_by_chunks(bin_len, self.lsb)
        return len_bits, arr_bits


class SteganoImageBaseSizedLSB4(SteganoImageBaseSizedLSB):
    def __init__(self, pic_file, data_file, use_shape_size: bool = False):
        super().__init__(pic_file, data_file, lsb=4, use_shape_size=use_shape_size)


class SteganoImageBaseSizedLSB2(SteganoImageBaseSizedLSB):
    def __init__(self, pic_file, data_file, use_shape_size: bool = False):
        super().__init__(pic_file, data_file, lsb=2, use_shape_size=use_shape_size)


class SteganoImageBaseSizedLSB1(SteganoImageBaseSizedLSB):
    def __init__(self, pic_file, data_file, use_shape_size: bool = False):
        super().__init__(pic_file, data_file, lsb=1, use_shape_size=use_shape_size)