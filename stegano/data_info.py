import glob
import os

from stegcrt.steg_lsb import *
from stegcrt.steg_sized import *

DATA_DIR = 'data/pics'
SRC_DIR = "data/archive"
FILES = glob.glob(SRC_DIR + "/**/*.jpg", recursive=True) + glob.glob(SRC_DIR + "/**/*.png", recursive=True)
FILES = [file.replace('\\', '/') for file in FILES]
BENIGN_DIR = "benign"
CLASSES = {'4_lsb': SteganoImage4LSB, '2_lsb': SteganoImage2LSB, '1_lsb': SteganoImage1LSB,
           'sized_4': SteganoImageBaseSizedLSB4, 'sized_2': SteganoImageBaseSizedLSB2,
           'sized_1': SteganoImageBaseSizedLSB1}
SIGNS = [BENIGN_DIR] + list(CLASSES.keys())
SIGNS_DICT = {SIGNS[i]: i for i in range(len(SIGNS))}
EXT = 'png'
MALWARE = 'malware'

class data_info:
    @staticmethod
    def make_dirs():
        for dir in SIGNS:
            try:
                os.makedirs(data_info.join_path(DATA_DIR, dir))
            except:
                continue

    @staticmethod
    def join_path(*args, ext: str = None):
        return os.path.join(*args).replace('\\', '/') + ('' if ext is None else f'.{ext}')
