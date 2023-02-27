from textwrap import wrap

from stegano_dec import get_messages

EVEN = 0
ODD = 1
PIX_LEN = 3
PIX_LOW = 0
PIX_HIGH = 255

# C:\Users\gilad\VirtualBox VMs\Ubuntu 20.04

def genData(data: str):
    # list of binary codes
    # of given data
    newd = []

    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd


print(genData("Hii"))


def change_value_num(num, mod):
    num = num % (PIX_HIGH + 1) + PIX_LOW  # pix vals
    if num % 2 == mod:
        return num
    if PIX_LOW <= num - 1 <= PIX_HIGH:
        return num - 1
    return num + 1


def change_pixel(pix, data: str):
    """
    gets a RGB pixel and string of 3 chars of 0 and 1 and change its values due to the mod
    pix - tuple of 3 ints
    data - string of 0 and 1
    """
    if len(pix) != PIX_LEN or len(data) != PIX_LEN:
        return None

    data = [int(i) for i in data]

    pix = [change_value_num(num, mod_val)
           for (num, mod_val) in zip(pix, data)]
    return tuple(pix)


def change_pixel_list(pix_list, data: str, is_last: bool):
    if len(pix_list) != 3 or len(data) != 8:
        return None

    data += '1' if is_last else '0'
    data = wrap(data, 3)
    pix_list = [change_pixel(pix, str_mod)
                for pix, str_mod in zip(pix_list, data)]
    return pix_list


def stegano_enc_messane_pix(message: str, pix_list: list):
    mess_list = genData(message)
    print(mess_list)
    if len(pix_list) < len(mess_list) * 3:
        return

    mess_list_len = len(mess_list)
    for i in range(mess_list_len):
        three_pix = pix_list[i * 3: (i + 1) * 3]

        three_pix = change_pixel_list(three_pix, mess_list[i], i == mess_list_len - 1)
        print(f"{three_pix}\t\t{mess_list[i]}")

        for j in range(3):
            pix_list[3 * i + j] = three_pix[j]



be = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (7, 8, 9)]

pix_list = [(27, 64, 164), (248, 244, 194), (174, 246, 250), (149, 95, 232),
            (188, 156, 169), (71, 167, 127), (132, 173, 97), (113, 69, 206),
            (255, 29, 213), (53, 153, 220), (246, 225, 229), (142, 82, 175)]
mess = 'Hii'

stegano_enc_messane_pix(mess, pix_list)
print(pix_list)

pix_check = [(26, 63, 164), (248, 243, 194), (174, 246, 250), (148, 95, 231),
            (188, 155, 168), (70, 167, 126), (132, 173, 97), (112, 69, 206),
            (254, 29, 213), (53, 153, 220), (246, 225, 229), (142, 82, 175)]

print (pix_list == pix_check)

print(get_messages(pix_list))

change_pixel_list(be[:3], '12345', True)
print(be)

print(wrap('1234', 3))









