import sys
import threading

from data_info import *
from tqdm import tqdm
import cv2
import random

from stegcrt.steg_lsb import *
from stegcrt.steg_sized import *

data_info.make_dirs()

def get_file_name(name: str):
    ind = name.rfind('/')
    if ind == -1:
        return '', ''
    name_final = name[ind + 1:]

    ind = name_final.rfind('.')
    if ind == -1:
        return name_final, ''

    ext = name_final[ind:]
    name_final = name_final[:ind]

    return name_final, ext

# NN = 4
# print(*CLASSES)

def make_pic_attack(files, count: int = 0, mal: bool = False, pbar: tqdm = None):
    my_len = len(files)

    if pbar is None:
        pbar = range(len(files))

    for i in pbar:
        file = files[i]
        name, ext = get_file_name(file)
        img = cv2.imread(file)
        pth = data_info.join_path(DATA_DIR, BENIGN_DIR, name, ext=EXT)
        cv2.imwrite(pth, img)
        # print(pth)
        #keys = list(CLASSES.keys())
        for attack in CLASSES.keys():        # list(keys[NN:NN])
            attack_lbl = MALWARE if mal else attack
            atk_pth = data_info.join_path(DATA_DIR, attack_lbl, name, ext=EXT)
            if os.path.exists(atk_pth):
                continue
            steg_mathod = CLASSES[attack](pth, utils.bin_random_all(100000))     # "data/alice_in_wonderland.txt"
            steg_mathod.perform_stegano(atk_pth)
        # if (i + 1) % 10 == 0:
        #     print(f'th No. {count}\t\t {i+1}/{my_len}')



# make_pic_attack(FILES)

mal = True
n = 2
parted = FILES[:3000]
len_f = len(parted)
n = int(len_f / n)
parted = [parted[i: i + n] for i in range(0, len_f, n)]

th_list = []
pbars = []
for i in range(len(parted)):
    files = parted[i]
    pbars += [tqdm(range(len(files)), desc=f"part {i}", position=i)]

for i in range(len(parted)):
    files = parted[i]
    # print(*files, sep='\n')
    # print("*"*100, '\n')
    # th = threading.Thread(target=make_pic_attack, args=(files, i, False, pbars[i]))
    # th.start()
    # th_list += [th]
    make_pic_attack(files, i, False, pbars[i])

# for th in th_list:
#     th.join()