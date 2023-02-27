from utils import *
from stegcrt.steg_base import SteganoImageBase
import cv2


class SteganoImageBaseLSB(SteganoImageBase):
    LGT_IN_PXL = 3

    def __init__(self, pic_file, data_file, lsb: int = 4, pos: int = 0):
        self.lsb = lsb
        self.pos = abs(pos) % self.LGT_IN_PXL
        self.mod = 2 ** self.lsb
        self.cnt_lsb = '0' * self.lsb
        self.brk_lsb = '1' * self.lsb
        super().__init__(pic_file, data_file)
        # print(self.list_bytes, f'\n{len(self.list_bytes)}\n')
        # divide it to groups by number of bytes

    def perform_stegano(self, name: str):
        parted_data, sized = self.parted_data_alg()
        # print(parted_data)
        steg = utils.inject_data_to_pixels(self.im_arr, parted_data, mod=self.mod)
        # ravel is iterable array that is 1-d  while the original form is not changed
        cv2.imwrite(name, steg)
        return int(sized * self.lsb / utils.BITS_IN_BYTE)

    def get_data(self, name):
        img = cv2.imread(name)
        return self.recover_data(img)

    def parted_data_alg(self):
        parted_data = utils.split_str_by_chunks(self.list_bytes, self.lsb)
        sized = int(self.im_arr.size * 2 / 3) - 1
        sized = min(sized, len(parted_data))
        sized -= sized % int(utils.BITS_IN_BYTE / self.lsb)
        parted_data = parted_data[:sized]
        new_parted = []
        counter = 0

        for d in parted_data:
            if counter == self.pos:
                new_parted.append(self.cnt_lsb)
                counter += 1
            new_parted.append(d)
            counter += 1
            counter %= self.LGT_IN_PXL
        stop_arr = [None, None, None]
        stop_arr[self.pos] = self.brk_lsb
        new_parted += stop_arr
        return new_parted, sized

    def recover_data(self, img):
        total = ''
        hidden = bytes()

        for pixel_data in img.reshape(-1, self.LGT_IN_PXL):
            pixel = []
            for n in pixel_data:
                pixel.append(utils.int_to_bin(n % self.mod, self.lsb))
            if pixel[self.pos] != self.cnt_lsb:
                break
            del pixel[self.pos]
            total += ''.join(pixel)
            if len(total) == utils.BITS_IN_BYTE:
                hidden += int(total, 2).to_bytes(1, 'big')
                total = ''
        return hidden


class SteganoImage4LSB(SteganoImageBaseLSB):
    def __init__(self, pic_file, data_file, pos: int = 0):
        super().__init__(pic_file, data_file, lsb=4, pos=pos)


class SteganoImage2LSB(SteganoImageBaseLSB):
    def __init__(self, pic_file, data_file, pos: int = 0):
        super().__init__(pic_file, data_file, lsb=2, pos=pos)


class SteganoImage1LSB(SteganoImageBaseLSB):
    def __init__(self, pic_file, data_file, pos: int = 0):
        super().__init__(pic_file, data_file, lsb=1, pos=pos)
