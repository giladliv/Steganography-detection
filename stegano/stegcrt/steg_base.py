from utils import *
import cv2


class SteganoImageBase:
    def __init__(self, pic_file, data_file):
        self.pic_file = pic_file
        self.data_file = data_file
        self.im_arr = cv2.imread(pic_file)
        # print(self.im_arr)
        self.list_bytes = []
        if type(data_file) is bytes:
            list_btye_str = [utils.byte_to_str_bin(byte) for byte in data_file]
            self.list_bytes = ''.join(list_btye_str)
        elif type(data_file) is str:
            self.list_bytes = utils.file_to_bin_str(data_file)
        else:
            raise RuntimeError("the data is nighter name of file nor bytes list")

    def perform_stegano(self, name: str):
        raise NotImplementedError('method "perform_stegano" has no implementation')

    def get_data(self, name):
        raise NotImplementedError('method "get_data" has no implementation')